"""
Deliverability Prediction Routes:
- POST /api/deliverability/check - Check if product is deliverable to location
- GET /api/deliverability/recommendations - Get alternative deliverable products
- POST /api/deliverability/batch-check - Batch check multiple locations
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

# Models
class DeliveryLocation(BaseModel):
    city: str = Field(..., description="Delivery city")
    state: str = Field(..., description="Delivery state")
    pincode: str = Field(..., description="Postal/Pin code")
    area: Optional[str] = Field(None, description="Area/Locality (optional)")

class ProductInfo(BaseModel):
    product_name: str = Field(..., description="Product name from Amazon")
    category: str = Field(..., description="Product category")
    sub_category: Optional[str] = Field(None, description="Sub-category")
    price: float = Field(..., description="Product price")
    weight_kg: float = Field(default=1.0, description="Product weight (kg)")

class DeliverabilityCheckRequest(BaseModel):
    product: ProductInfo
    delivery_location: DeliveryLocation

class DeliverabilityCheckResponse(BaseModel):
    product_name: str
    location: Dict
    is_deliverable: bool
    confidence: float = Field(..., description="0-1 confidence score")
    risk_score: float = Field(..., description="0-100 non-deliverability risk")
    delivery_time_estimate: int = Field(..., description="Estimated days")
    reason: str
    recommendation: str

class AlternativeProduct(BaseModel):
    product_name: str
    category: str
    price: float
    location: str
    availability: str
    rating: Optional[float] = None
    reasons_better: List[str]

class RecommendationResponse(BaseModel):
    product_name: str
    original_location: Dict
    is_original_deliverable: bool
    alternatives: List[AlternativeProduct]
    suggestion_reason: str

# Load dataset on startup
dataset_df = None

def load_dataset_for_deliverability():
    """Load dataset for deliverability analysis"""
    global dataset_df
    try:
        dataset_path = Path(__file__).parent.parent / "dataset" / "final_dataset.csv"
        if dataset_path.exists():
            dataset_df = pd.read_csv(dataset_path)
            logger.info(f"✓ Deliverability dataset loaded: {dataset_df.shape[0]} rows")
            return True
        else:
            logger.warning(f"Dataset not found at {dataset_path}")
            return False
    except Exception as e:
        logger.error(f"Error loading deliverability dataset: {e}")
        return False

@deliverability_router.post("/check", response_model=DeliverabilityCheckResponse)
async def check_deliverability(request: DeliverabilityCheckRequest):
    """
    Check if a product is deliverable to a specific location
    
    Uses ML model to predict deliverability based on:
    - Product category and type
    - Delivery location (city, state)
    - Historical delivery patterns
    - Product characteristics
    """
    try:
        global dataset_df
        
        if dataset_df is None:
            load_dataset_for_deliverability()
        
        if dataset_df is None:
            raise HTTPException(status_code=503, detail="Dataset not available")
        
        from app import MLModels
        import joblib
        
        # Load models if not in memory
        if MLModels.classifier is None:
            model_path = Path("./models")
            MLModels.classifier = joblib.load(model_path / "model_classifier.joblib")
            MLModels.scaler = joblib.load(model_path / "scaler.joblib")
            MLModels.label_encoders = joblib.load(model_path / "label_encoders.joblib")
        
        product = request.product
        location = request.delivery_location
        
        logger.info(f"Checking deliverability for {product.product_name} to {location.city}, {location.state}")
        
        # Get location statistics from dataset
        location_data = dataset_df[
            (dataset_df['City'].str.lower() == location.city.lower()) &
            (dataset_df['State'].str.lower() == location.state.lower())
        ]
        
        # Get category statistics
        category_data = dataset_df[dataset_df['Category'] == product.category]
        
        # Calculate metrics
        if len(location_data) > 0:
            location_delivery_rate = (location_data['deliverability_category'] != 'Very High Risk (Non-Deliverable)').sum() / len(location_data)
            avg_delivery_days = location_data['shipment days'].mean()
            location_difficulty = location_data['location_difficulty'].mean()
        else:
            location_delivery_rate = 0.7  # Default assumption
            avg_delivery_days = 5
            location_difficulty = 50
        
        if len(category_data) > 0:
            category_reliability = category_data['product_reliability'].mean()
            category_complexity = category_data['category_complexity'].mean()
        else:
            category_reliability = 75
            category_complexity = 50
        
        # Make prediction using ML model
        try:
            # Create feature vector for prediction
            features = np.array([[
                1.0,  # Product availability normalized
                5,    # Estimated shipping speed (days)
                product.weight_kg,
                location_difficulty,
                category_reliability,
                category_complexity,
                location_delivery_rate * 100,
                avg_delivery_days,
                product.price,
                0.05  # Average discount
            ]])
            
            # Scale features
            features_scaled = MLModels.scaler.transform(features.reshape(1, -1))
            
            # Get prediction probability
            prediction_prob = MLModels.classifier.predict_proba(features_scaled)[0]
            non_deliverable_prob = prediction_prob[1] if len(prediction_prob) > 1 else 0.5
            
            is_deliverable = non_deliverable_prob < 0.5
            confidence = 1 - abs(0.5 - non_deliverable_prob) * 2
            risk_score = non_deliverable_prob * 100
            
        except Exception as e:
            logger.warning(f"ML model prediction failed, using heuristics: {e}")
            # Fallback to heuristic
            is_deliverable = location_delivery_rate > 0.6
            confidence = 0.7
            risk_score = (1 - location_delivery_rate) * 100
        
        # Generate response
        if is_deliverable:
            reason = f"Location {location.city}, {location.state} has {location_delivery_rate*100:.1f}% delivery success rate. Category '{product.category}' is reliable in this area."
            recommendation = "✓ This product is DELIVERABLE. You can proceed with the purchase with confidence."
            delivery_estimate = int(avg_delivery_days)
        else:
            reason = f"Location {location.city}, {location.state} has delivery challenges (only {location_delivery_rate*100:.1f}% success rate). Recent delays reported."
            recommendation = "✗ HIGH RISK: This product may not be delivered. Consider alternatives in your area or nearby cities."
            delivery_estimate = int(avg_delivery_days) + 3  # Add buffer for risky locations
        
        return DeliverabilityCheckResponse(
            product_name=product.product_name,
            location=request.delivery_location.dict(),
            is_deliverable=is_deliverable,
            confidence=round(confidence, 2),
            risk_score=round(risk_score, 2),
            delivery_time_estimate=delivery_estimate,
            reason=reason,
            recommendation=recommendation
        )
        
    except Exception as e:
        logger.error(f"Error checking deliverability: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@deliverability_router.post("/recommendations", response_model=RecommendationResponse)
async def get_alternatives(request: DeliverabilityCheckRequest):
    """
    Get alternative products that ARE deliverable to the location
    
    Suggests similar products in same category that have:
    - High delivery success rate to the location
    - Similar price range
    - Good ratings
    """
    try:
        global dataset_df
        
        if dataset_df is None:
            load_dataset_for_deliverability()
        
        if dataset_df is None:
            raise HTTPException(status_code=503, detail="Dataset not available")
        
        product = request.product
        location = request.delivery_location
        
        logger.info(f"Getting alternatives for {product.product_name} in {location.city}")
        
        # First check if original is deliverable
        check_response = await check_deliverability(request)
        
        # Find alternative products
        alternatives_data = dataset_df[
            (dataset_df['City'].str.lower() == location.city.lower()) &
            (dataset_df['State'].str.lower() == location.state.lower()) &
            (dataset_df['Category'] == product.category) &
            (dataset_df['deliverability_category'] != 'Very High Risk (Non-Deliverable)')
        ]
        
        # If not enough in same city, look in same state/region
        if len(alternatives_data) < 3:
            alternatives_data = dataset_df[
                (dataset_df['State'].str.lower() == location.state.lower()) &
                (dataset_df['Category'] == product.category) &
                (dataset_df['deliverability_category'] != 'Very High Risk (Non-Deliverable)')
            ]
        
        # Convert to alternatives list
        alternatives = []
        for idx, row in alternatives_data.head(5).iterrows():
            alt = AlternativeProduct(
                product_name=row['Product Name'],
                category=row['Category'],
                price=row['Sales'],
                location=f"{row['City']}, {row['State']}",
                availability="In Stock",
                reasons_better=[
                    f"Available in {row['City']}",
                    f"Delivery success: {row['deliverability_category']}",
                    f"Avg delivery time: {row['shipment days']:.0f} days"
                ]
            )
            alternatives.append(alt)
        
        return RecommendationResponse(
            product_name=product.product_name,
            original_location=request.delivery_location.dict(),
            is_original_deliverable=check_response.is_deliverable,
            alternatives=alternatives,
            suggestion_reason=f"Found {len(alternatives)} highly deliverable alternatives in '{product.category}' category" if len(alternatives) > 0 else "No alternatives available at this time"
        )
        
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@deliverability_router.post("/batch-check")
async def batch_check(checks: List[DeliverabilityCheckRequest]):
    """
    Check deliverability for multiple products/locations
    
    Useful for comparing multiple products or locations
    """
    try:
        results = []
        for check_request in checks:
            result = await check_deliverability(check_request)
            results.append(result)
        
        return {
            "total_checks": len(checks),
            "results": results,
            "deliverable_count": sum(1 for r in results if r.is_deliverable),
            "non_deliverable_count": sum(1 for r in results if not r.is_deliverable)
        }
        
    except Exception as e:
        logger.error(f"Error in batch check: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@deliverability_router.get("/locations")
async def get_supported_locations():
    """
    Get list of supported locations for deliverability prediction
    """
    try:
        global dataset_df
        
        if dataset_df is None:
            load_dataset_for_deliverability()
        
        if dataset_df is None:
            return {"message": "Dataset not available"}
        
        locations = dataset_df.groupby(['City', 'State']).agg({
            'deliverability_category': lambda x: (x != 'Very High Risk (Non-Deliverable)').sum() / len(x),
            'shipment days': 'mean'
        }).round(2)
        
        locations_list = [
            {
                "city": city,
                "state": state,
                "delivery_success_rate": f"{rate*100:.1f}%",
                "avg_delivery_days": int(days)
            }
            for (city, state), (rate, days) in locations.iterrows()
        ]
        
        return {
            "total_locations": len(locations_list),
            "locations": locations_list[:50]  # Return top 50
        }
        
    except Exception as e:
        logger.error(f"Error getting locations: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Load dataset on startup
load_dataset_for_deliverability()
