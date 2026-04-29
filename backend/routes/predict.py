"""
Prediction API Routes:
- POST /api/predict - Make prediction for a single product
- POST /api/batch_predict - Batch predictions
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import numpy as np
import logging
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = logging.getLogger(__name__)
predict_router = APIRouter()

# Request/Response Models
class PredictionRequest(BaseModel):
    product_id: str = Field(..., description="Unique product identifier")
    product_category: str = Field(..., description="Product category")
    product_age_days: int = Field(..., description="Days since product added")
    sales_velocity: float = Field(..., description="Sales per day")
    order_count: int = Field(..., description="Total order count")
    return_rate: float = Field(..., ge=0, le=1, description="Return rate 0-1")
    review_score: float = Field(..., ge=1, le=5, description="Average review score")
    avg_delivery_days: float = Field(..., description="Average delivery time in days")
    warehouse_distance_km: float = Field(..., description="Distance to warehouse in km")
    city: str = Field(..., description="Delivery city")
    state: str = Field(..., description="Delivery state")
    weight_kg: float = Field(..., description="Product weight in kg")
    dimensions_volume_cm3: float = Field(..., description="Volume in cm3")

    class Config:
        schema_extra = {
            "example": {
                "product_id": "PROD_12345",
                "product_category": "Electronics",
                "product_age_days": 120,
                "sales_velocity": 5.5,
                "order_count": 250,
                "return_rate": 0.05,
                "review_score": 4.2,
                "avg_delivery_days": 3.5,
                "warehouse_distance_km": 150,
                "city": "Mumbai",
                "state": "Maharashtra",
                "weight_kg": 0.5,
                "dimensions_volume_cm3": 1000
            }
        }

class PredictionResponse(BaseModel):
    product_id: str
    deliverability_probability: float = Field(..., description="0-1 probability of successful delivery")
    risk_score: float = Field(..., description="0-100 risk score")
    prediction_category: str = Field(..., description="Very High, High, Medium, Low")
    confidence: float = Field(..., description="Model confidence 0-1")
    recommendation: str = Field(..., description="Action recommendation")

@predict_router.post("/predict", response_model=PredictionResponse)
async def predict_delivery(request: PredictionRequest):
    """
    Make a single prediction for product deliverability
    
    Returns:
    - deliverability_probability: Likelihood of successful delivery (0-1)
    - risk_score: Non-deliverable risk on 0-100 scale
    - prediction_category: Risk category (Very High, High, Medium, Low)
    - confidence: Model confidence in prediction
    - recommendation: Action to take based on prediction
    """
    
    try:
        from app import MLModels
        import joblib
        from pathlib import Path
        
        # If models not already loaded, load them now
        if MLModels.classifier is None:
            logger.info("Models not in memory, loading from disk...")
            model_path = Path("./models")
            MLModels.classifier = joblib.load(model_path / "model_classifier.joblib")
            MLModels.regressor = joblib.load(model_path / "model_regressor.joblib")
            MLModels.scaler = joblib.load(model_path / "scaler.joblib")
            MLModels.label_encoders = joblib.load(model_path / "label_encoders.joblib")
            logger.info("✓ Models loaded successfully!")
        
        logger.info(f"Using models - Classifier type: {type(MLModels.classifier)}, Scaler features: {MLModels.scaler.n_features_in_}")
        
        # Build initial feature list from incoming request (core numeric inputs)
        base_features = [
            request.product_age_days,
            request.sales_velocity,
            request.order_count,
            request.return_rate,
            request.review_score,
            request.avg_delivery_days,
            request.warehouse_distance_km,
            request.weight_kg,
            request.dimensions_volume_cm3,
        ]

        expected_n = getattr(MLModels.scaler, 'n_features_in_', None)
        if expected_n is None:
            # fallback to current length of base features
            expected_n = len(base_features)

        # If scaler expects more features, pad with zeros; if fewer, truncate
        if expected_n > len(base_features):
            pad = [0.0] * (expected_n - len(base_features))
            features_list = base_features + pad
        else:
            features_list = base_features[:expected_n]

        features = np.array([features_list], dtype=np.float64)
        logger.info(f"Features array shape before align: {features.shape}")

        # Ensure feature vector matches scaler's expected input size
        try:
            expected = int(MLModels.scaler.n_features_in_)
        except Exception:
            expected = None

        if expected is not None:
            current = features.shape[1]
            if current < expected:
                # pad with zeros to match expected size
                pad_width = expected - current
                logger.warning(f"Feature length {current} < expected {expected}, padding {pad_width} zeros")
                features = np.hstack([features, np.zeros((1, pad_width), dtype=np.float64)])
            elif current > expected:
                # truncate extra features
                logger.warning(f"Feature length {current} > expected {expected}, truncating to {expected}")
                features = features[:, :expected]

        logger.info(f"Features array shape after align: {features.shape}")

        # Scale features using the trained scaler
        try:
            scaled_features = MLModels.scaler.transform(features)
        except Exception as e:
            logger.error(f"Scaler transform failed: {e}")
            raise
        logger.info(f"Scaled features shape: {scaled_features.shape}")
        
        # Get classifier prediction (5 classes: 0-4)
        classifier_pred = MLModels.classifier.predict(scaled_features)[0]
        classifier_proba = MLModels.classifier.predict_proba(scaled_features)[0]
        
        # Get regressor prediction (risk score)
        risk_score_raw = MLModels.regressor.predict(scaled_features)[0]
        risk_score = float(np.clip(risk_score_raw, 0, 100))
        
        # Calculate deliverability probability (inverse of risk)
        deliverability_probability = float(1.0 - (risk_score / 100.0))
        
        # Get class probabilities
        max_prob = float(np.max(classifier_proba))
        
        # Determine risk level based on regressor output
        if risk_score >= 75:
            prediction_category = "Very High Risk"
            confidence = min(max_prob * 100, 95)
            recommendation = "HOLD_SHIPMENT - Requires manual intervention"
        elif risk_score >= 50:
            prediction_category = "High Risk"
            confidence = min(max_prob * 100, 90)
            recommendation = "ENHANCED_TRACKING - Monitor closely"
        elif risk_score >= 25:
            prediction_category = "Medium Risk"
            confidence = min(max_prob * 100, 85)
            recommendation = "STANDARD_HANDLING - No special measures needed"
        else:
            prediction_category = "Low Risk"
            confidence = min(max_prob * 100, 95)
            recommendation = "EXPEDITE - Safe for fast track delivery"
        
        logger.info(f"Prediction successful: risk_score={risk_score}, category={prediction_category}")
        
        return PredictionResponse(
            product_id=request.product_id,
            deliverability_probability=round(deliverability_probability, 4),
            risk_score=round(risk_score, 2),
            prediction_category=prediction_category,
            confidence=round(float(confidence), 2),
            recommendation=recommendation
        )
        
    except ValueError as e:
        logger.error(f"Feature validation error: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid input data: {str(e)}")
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

class BatchPredictionRequest(BaseModel):
    predictions: List[PredictionRequest]

@predict_router.post("/batch_predict")
async def batch_predict(request: BatchPredictionRequest):
    """
    Make batch predictions for multiple products
    
    Returns list of predictions with same format as /predict endpoint
    """
    if len(request.predictions) > 1000:
        raise HTTPException(status_code=400, detail="Batch size limited to 1000 products")
    
    results = []
    for pred_request in request.predictions:
        try:
            result = await predict_delivery(pred_request)
            results.append(result)
        except HTTPException as e:
            results.append({
                "product_id": pred_request.product_id,
                "error": e.detail
            })
    
    return {"total": len(request.predictions), "results": results}

@predict_router.get("/predict_schema")
async def get_prediction_schema():
    """Get prediction request schema"""
    return {
        "request": PredictionRequest.schema(),
        "response": PredictionResponse.schema()
    }
