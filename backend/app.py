"""
Main FastAPI Application - Non-Deliverable Prediction System
Loads trained ML models and provides REST API endpoints for predictions
"""

import os
import sys
import joblib
import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Ensure backend path is in sys.path for imports
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Non-Deliverable Prediction API",
    description="ML-powered API for predicting product delivery failures and recommendations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model storage
class MLModels:
    classifier = None
    regressor = None
    scaler = None
    label_encoders = None

def load_models():
    """Load all trained ML models from joblib files"""
    try:
        model_path = Path(os.getenv("MODEL_PATH", "./models"))
        
        logger.info("Loading ML models...")
        
        # Load classifier
        classifier_path = model_path / os.getenv("CLASSIFIER_MODEL", "model_classifier.joblib")
        MLModels.classifier = joblib.load(classifier_path)
        logger.info(f"✓ Classifier loaded: {classifier_path}")
        
        # Load regressor
        regressor_path = model_path / os.getenv("REGRESSOR_MODEL", "model_regressor.joblib")
        MLModels.regressor = joblib.load(regressor_path)
        logger.info(f"✓ Regressor loaded: {regressor_path}")
        
        # Load scaler
        scaler_path = model_path / os.getenv("SCALER_MODEL", "scaler.joblib")
        MLModels.scaler = joblib.load(scaler_path)
        logger.info(f"✓ Scaler loaded: {scaler_path}")
        
        # Load label encoders
        encoder_path = model_path / os.getenv("ENCODER_MODEL", "label_encoders.joblib")
        MLModels.label_encoders = joblib.load(encoder_path)
        logger.info(f"✓ Label encoders loaded: {encoder_path}")
        
        logger.info("✓ All models loaded successfully!")
        return True
        
    except FileNotFoundError as e:
        logger.error(f"✗ Model file not found: {e}")
        return False
    except Exception as e:
        logger.error(f"✗ Error loading models: {e}")
        return False

@app.on_event("startup")
async def startup_event():
    """Load models and dataset when application starts"""
    logger.info("=" * 80)
    logger.info("STARTING UP - Loading Models and Dataset")
    logger.info("=" * 80)
    
    if not load_models():
        logger.warning("⚠ Models failed to load - API will not make predictions")
    
    # Load dataset
    from routes.dataset import load_dataset
    if not load_dataset():
        logger.warning("⚠ Dataset failed to load - dataset endpoints will not work")
    
    logger.info("=" * 80)
    logger.info("STARTUP COMPLETE")
    logger.info("=" * 80)

@app.get("/")
async def root():
    """Root endpoint - API status"""
    models_loaded = (
        MLModels.classifier is not None and 
        MLModels.regressor is not None and 
        MLModels.scaler is not None and 
        MLModels.label_encoders is not None
    )
    
    return {
        "service": "Non-Deliverable Prediction API",
        "version": "1.0.0",
        "status": "running",
        "models_loaded": models_loaded,
        "endpoints": {
            "prediction": "/api/predict",
            "recommendations": "/api/recommendations/{product_id}",
            "analytics": "/api/analytics",
            "dataset_info": "/api/dataset/info",
            "dataset_products": "/api/dataset/products",
            "dataset_search": "/api/dataset/search",
            "dataset_stats": "/api/dataset/stats",
            "ecommerce_flipkart": "/api/ecommerce/flipkart?query=laptop&limit=10",
            "ecommerce_amazon": "/api/ecommerce/amazon?query=phone&limit=10",
            "ecommerce_search": "/api/ecommerce/search?query=laptop&limit=5&platforms=both",
            "ecommerce_compare": "/api/ecommerce/compare?query=laptop&limit=5",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    models_loaded = (
        MLModels.classifier is not None and 
        MLModels.regressor is not None
    )
    
    if not models_loaded:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    return {"status": "healthy", "models_loaded": models_loaded}

@app.get("/docs", include_in_schema=False)
async def get_docs():
    """API documentation redirect"""
    return {"message": "Visit /docs for API documentation"}

# Import routes after app initialization
from routes.predict import predict_router
from routes.recommendations import recommendations_router
from routes.dataset import dataset_router, load_dataset
from routes.ecommerce import ecommerce_router
from routes.advanced_deliverability import deliverability_router

# Include routers
app.include_router(predict_router, prefix="/api", tags=["predictions"])
app.include_router(recommendations_router, prefix="/api", tags=["recommendations"])
app.include_router(dataset_router, prefix="", tags=["dataset"])
app.include_router(ecommerce_router, prefix="/api/ecommerce", tags=["ecommerce"])
app.include_router(deliverability_router, prefix="/api/deliverability", tags=["deliverability-v2"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000))
    )
