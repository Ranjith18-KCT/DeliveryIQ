"""
Enhanced Deliverability Routes using Three-Tier ML System
- Tier 1: XGBoost Classifier (Is it deliverable?)
- Tier 2: Recommendation Engine (What alternatives?)
- Tier 3: Random Forest Regressor (When will it arrive?)
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import pandas as pd
import numpy as np
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)
deliverability_router = APIRouter()

# Data Models
class DeliveryLocation(BaseModel):
    city: str = Field(..., description="Delivery city")
    state: str = Field(..., description="Delivery state")
    pincode: str = Field(..., description="Postal/Pin code")
    area: Optional[str] = Field(None, description="Area/Locality (optional)")

class ProductInfo(BaseModel):
    product_name: str = Field(..., description="Product name from Amazon")
    category: str = Field(..., description="Product category")
    price: float = Field(..., description="Product price")
    weight_kg: float = Field(default=1.0, description="Product weight (kg)")
    rating: Optional[float] = Field(None, description="Product rating")

class DeliverabilityCheckRequest(BaseModel):
    product: ProductInfo
    delivery_location: DeliveryLocation

class TierResult(BaseModel):
    tier: str
    model_name: str
    result: Dict

class DeliverabilityCheckResponse(BaseModel):
    product_name: str
    location: Dict
    tier_1_classification: Dict  # XGBoost result
    tier_2_recommendations: Optional[List[Dict]] = None  # Only if not deliverable
    tier_3_delivery_time: Optional[Dict] = None  # Only if deliverable
    final_verdict: str
    confidence: float
    risk_score: float

class AlternativeProduct(BaseModel):
    product_name: str
    category: str
    price: float
    rating: Optional[float]
    location: str
    availability: str
    reasons_better: List[str]

# Global variables
dataset_df = None
advanced_model = None

def load_dataset():
    """Load dataset for recommendations"""
    global dataset_df
    try:
        dataset_path = Path(__file__).parent.parent / "dataset" / "final_dataset.csv"
        if dataset_path.exists():
            dataset_df = pd.read_csv(dataset_path)
            logger.info(f"✓ Deliverability dataset loaded: {dataset_df.shape[0]} rows")
            return True
    except Exception as e:
        logger.error(f"Error loading dataset: {e}")
    return False

def load_advanced_model():
    """Load the three-tier ML system"""
    global advanced_model
    try:
        from advanced_deliverability_model import AdvancedDeliverabilityModel
        
        advanced_model = AdvancedDeliverabilityModel()
        if advanced_model.load_models():
            logger.info("✓ Advanced ML models loaded (XGBoost + Random Forest)")
            return True
        else:
            raise Exception("Failed to load models")
    except Exception as e:
        logger.error(f"Error loading advanced model: {e}")
        return False

# Initialize on startup
@deliverability_router.on_event("startup")
async def startup():
    """Initialize models on startup"""
    load_dataset()
    load_advanced_model()

@deliverability_router.post("/check", response_model=DeliverabilityCheckResponse)
async def check_deliverability(request: DeliverabilityCheckRequest):
    """
    Three-Tier Deliverability Prediction System
    
    TIER 1: Classification (XGBoost Classifier)
    - Determines if product is deliverable
    - Based on: distance, weight, category, logistics
    - Output: is_deliverable (boolean), confidence
    
    TIER 2: Recommendation (if Tier 1 = Not Deliverable)
    - Suggests similar alternative products
    - Based on: category, location, price, ratings
    - Output: list of alternatives
    
    TIER 3: Regression (if Tier 1 = Deliverable)
    - Predicts delivery time in days
    - Based on: shipping speed, distance, logistics
    - Output: estimated_delivery_days
    """
    try:
        global dataset_df, advanced_model
        
        if dataset_df is None:
            load_dataset()
        if advanced_model is None:
            load_advanced_model()
        
        if advanced_model is None:
            raise HTTPException(status_code=503, detail="ML models not available")
        
        product = request.product
        location = request.delivery_location
        
        logger.info(f"≫ TIER 1 CHECK: {product.product_name} → {location.city}, {location.state}")
        
        # ============================================================================
        # TIER 1: CLASSIFICATION - Is product deliverable?
        # ============================================================================
        
        # Extract features for the product-location pair
        location_data = dataset_df[
            (dataset_df['City'].str.lower() == location.city.lower()) &
            (dataset_df['State'].str.lower() == location.state.lower())
        ] if dataset_df is not None else pd.DataFrame()
        
        # Build feature vector
        location_difficulty = location_data['location_difficulty'].mean() if len(location_data) > 0 else 50
        shipping_speed = location_data['shipment days'].mean() if len(location_data) > 0 else 5
        seller_reliability = location_data['seller_reliability'].mean() if len(location_data) > 0 else 75
        category_reliability = dataset_df[dataset_df['Category'] == product.category]['product_reliability'].mean() if dataset_df is not None and 'Category' in dataset_df.columns else 75
        category_complexity = dataset_df[dataset_df['Category'] == product.category]['category_complexity'].mean() if dataset_df is not None and 'Category' in dataset_df.columns else 50
        success_rate = location_data['success_rate'].mean() if len(location_data) > 0 else 0.75
        
        features = np.array([[
            location_difficulty,
            product.weight_kg,
            min(product.price / 1000, 50),  # Normalize price
            shipping_speed,
            seller_reliability / 100,
            category_reliability / 100,
            category_complexity / 100,
            1.0,  # availability_score
            success_rate,
            location_difficulty * 10,  # estimated_distance
            (location_difficulty + category_complexity * 50) / 2  # combined_score
        ]])
        
        # Get classification prediction
        classification_result = advanced_model.predict_deliverability(features)
        
        tier_1_result = {
            'model': 'XGBoost Classifier',
            'is_deliverable': classification_result['is_deliverable'],
            'deliverable_probability': round(classification_result['deliverable_probability'], 3),
            'non_deliverable_probability': round(classification_result['non_deliverable_probability'], 3),
            'confidence': round(classification_result['confidence'], 3),
            'risk_score': round(classification_result['risk_score'], 1)
        }
        
        reason = (
            f"✓ LIKELY DELIVERABLE ({tier_1_result['deliverable_probability']*100:.1f}% confidence) - "
            f"{location.city}, {location.state} has good delivery infrastructure for this category."
        ) if classification_result['is_deliverable'] else (
            f"✗ HIGH RISK ({tier_1_result['non_deliverable_probability']*100:.1f}% probability) - "
            f"Delivery to {location.city}, {location.state} poses logistics challenges. Consider alternatives."
        )
        
        recommendations_tier2 = None
        delivery_time_tier3 = None
        
        # ============================================================================
        # TIER 2: RECOMMENDATIONS - Get alternatives if not deliverable
        # ============================================================================
        
        if not classification_result['is_deliverable']:
            logger.info(f"≫ TIER 2 RECOMMENDATIONS: Finding alternatives...")
            
            recommendations_tier2 = _get_alternatives(product, location)
            
            reason += "\n\nRECOMMENDED ALTERNATIVES:"
            for alt in recommendations_tier2[:3]:
                reason += f"\n• {alt['product_name']} (₹{alt['price']}, Rating: {alt.get('rating', 'N/A')})"
        
        # ============================================================================
        # TIER 3: DELIVERY TIME PREDICTION - Estimate delivery if deliverable
        # ============================================================================
        
        else:
            logger.info(f"≫ TIER 3 REGRESSION: Predicting delivery time...")
            
            delivery_time_result = advanced_model.predict_delivery_time(features)
            
            delivery_time_tier3 = {
                'model': 'Random Forest Regressor',
                'estimated_delivery_days': delivery_time_result['estimated_delivery_days'],
                'confidence': round(delivery_time_result['confidence'], 3),
                'estimated_delivery_date': f"In {delivery_time_result['estimated_delivery_days']} days"
            }
            
            reason += f"\n\nESTIMATED DELIVERY: {delivery_time_result['estimated_delivery_days']} days ({delivery_time_tier3['estimated_delivery_date']})"
        
        # ============================================================================
        # FINAL RESPONSE
        # ============================================================================
        
        return DeliverabilityCheckResponse(
            product_name=product.product_name,
            location=request.delivery_location.dict(),
            tier_1_classification=tier_1_result,
            tier_2_recommendations=recommendations_tier2,
            tier_3_delivery_time=delivery_time_tier3,
            final_verdict="DELIVERABLE" if classification_result['is_deliverable'] else "NOT DELIVERABLE",
            confidence=round(classification_result['confidence'], 3),
            risk_score=round(classification_result['risk_score'], 1)
        )
        
    except Exception as e:
        logger.error(f"Error in deliverability check: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

def _get_alternatives(product: ProductInfo, location: DeliveryLocation) -> List[Dict]:
    """
    TIER 2: Find alternative products that are deliverable
    Uses the dataset to find similar products with high delivery success
    """
    global dataset_df
    
    if dataset_df is None:
        return []
    
    try:
        # Filter for deliverable products in same location and category
        alternatives = dataset_df[
            (dataset_df['City'].str.lower() == location.city.lower()) &
            (dataset_df['deliverability_category'] != 'Very High Risk (Non-Deliverable)') &
            (dataset_df.get('Category', product.category) == product.category if 'Category' in dataset_df.columns else True)
        ].drop_duplicates(subset=['Product Name'])
        
        # If not enough, search in same state
        if len(alternatives) < 3:
            alternatives = dataset_df[
                (dataset_df['State'].str.lower() == location.state.lower()) &
                (dataset_df['deliverability_category'] != 'Very High Risk (Non-Deliverable)') &
                (dataset_df.get('Category', product.category) == product.category if 'Category' in dataset_df.columns else True)
            ].drop_duplicates(subset=['Product Name'])
        
        # Convert to list of dict (up to 20 products for filtering options)
        result = []
        for idx, row in alternatives.head(20).iterrows():
            reason_better = []
            
            if row.get('price', product.price) < product.price:
                reason_better.append(f"₹{row.get('price', 'N/A')} (cheaper)")
            if row.get('rating', 0) > (product.rating or 0):
                reason_better.append(f"Higher rating: {row.get('rating', 'N/A')} stars")
            if row.get('success_rate', 0.7) > 0.8:
                reason_better.append("High delivery success rate")
            
            # Generate random product image URL from valid sources
            image_url = f"https://via.placeholder.com/200x200?text={row.get('Product Name', 'Product')[:20].replace(' ', '+')}"
            if 'image' in row and pd.notna(row['image']):
                image_url = row['image']
            else:
                # Use category-based placeholder
                categories = ['Electronics', 'Books', 'Clothing', 'Home', 'Sports']
                category = str(row.get('Category', 'Product')).lower()
                color = 'FF6B6B' if 'electronics' in category else '4ECDC4' if 'book' in category else 'FFE66D' if 'cloth' in category else '95E1D3'
                image_url = f"https://via.placeholder.com/200x200?text={category[:15]}&bg={color}&txtcolor=000000"
            
            result.append({
                'product_name': row.get('Product Name', 'Unknown'),
                'category': row.get('Category', product.category),
                'price': round(float(row.get('price', product.price)), 2),
                'rating': round(float(row.get('rating', 0)), 1) if pd.notna(row.get('rating')) else None,
                'location': f"{row.get('City', location.city)}, {row.get('State', location.state)}",
                'availability': row.get('availability', 'In Stock'),
                'reasons_better': reason_better if reason_better else ["Deliverable to your location"],
                'image_url': image_url
            })
        
        logger.info(f"✓ Found {len(result)} alternative products")
        return result
        
    except Exception as e:
        logger.error(f"Error getting alternatives: {e}")
        return []

@deliverability_router.get("/locations")
async def get_supported_locations():
    """Get list of supported delivery locations"""
    global dataset_df
    
    if dataset_df is None:
        load_dataset()
    
    if dataset_df is None:
        raise HTTPException(status_code=503, detail="Dataset not loaded")
    
    try:
        locations = dataset_df.drop_duplicates(subset=['City', 'State']).head(100)
        
        result = [
            {
                'city': row['City'],
                'state': row['State'],
                'delivery_success_rate': round(
                    ((row['deliverability_category'] != 'Very High Risk (Non-Deliverable)') * 100), 1
                ) if 'deliverability_category' in row else 75
            }
            for _, row in locations.iterrows()
        ]
        
        return {
            'total_locations': len(result),
            'locations': sorted(result, key=lambda x: x['delivery_success_rate'], reverse=True)
        }
    except Exception as e:
        logger.error(f"Error fetching locations: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@deliverability_router.post("/batch-check")
async def batch_check(requests: List[DeliverabilityCheckRequest]):
    """Check deliverability for multiple products"""
    results = []
    for req in requests:
        try:
            result = await check_deliverability(req)
            results.append(result)
        except Exception as e:
            logger.error(f"Error batch checking: {e}")
            results.append({"error": str(e)})
    
    return {
        'total_checked': len(requests),
        'results': results
    }
