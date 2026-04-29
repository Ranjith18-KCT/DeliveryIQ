"""
Configuration settings for different environments
"""

import os
from enum import Enum

class Environment(str, Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"

class Config:
    """Base configuration"""
    ENV = os.getenv("ENVIRONMENT", "development")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))
    WORKERS = 4
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL")
    DB_POOL_SIZE = 5
    DB_MAX_OVERFLOW = 10
    DB_ECHO = False
    
    # Models
    MODEL_PATH = os.getenv("MODEL_PATH", "./models")
    CLASSIFIER_MODEL = os.getenv("CLASSIFIER_MODEL", "model_classifier.joblib")
    REGRESSOR_MODEL = os.getenv("REGRESSOR_MODEL", "model_regressor.joblib")
    SCALER_MODEL = os.getenv("SCALER_MODEL", "scaler.joblib")
    ENCODER_MODEL = os.getenv("ENCODER_MODEL", "label_encoders.joblib")
    
    # Frontend
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
    ALLOWED_ORIGINS = [
        FRONTEND_URL,
        "https://ecommerce-predictor.netlify.app",
        "http://localhost:3000",
        "http://localhost:3001"
    ]
    
    # Prediction Settings
    DELIVERY_RISK_THRESHOLD = 0.5
    LOW_CONFIDENCE_THRESHOLD = 0.7
    BATCH_PREDICTION_LIMIT = 1000
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Cache
    CACHE_ENABLED = True
    CACHE_TTL = 3600  # seconds

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    DB_ECHO = True
    LOG_LEVEL = "DEBUG"
    CACHE_ENABLED = False
    
class TestingConfig(Config):
    """Testing environment configuration"""
    DATABASE_URL = "postgresql://test:test@localhost:5432/ecommerce_test"
    DEBUG = True
    DB_ECHO = False
    LOG_LEVEL = "INFO"
    
class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    DB_ECHO = False
    LOG_LEVEL = "WARNING"
    WORKERS = 8
    DB_POOL_SIZE = 20
    DB_MAX_OVERFLOW = 20

# Configuration factory
def get_config():
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    configs = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig
    }
    
    return configs.get(env, DevelopmentConfig)

# Get active configuration
config = get_config()
