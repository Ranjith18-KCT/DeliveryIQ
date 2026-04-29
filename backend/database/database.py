"""
Database Connection and ORM Models
PostgreSQL connection pooling and SQLAlchemy models
"""

import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/ecommerce_db")

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    echo=False,
    connect_args={"connect_timeout": 10}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base for models
Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============ ORM Models ============

class Product(Base):
    """Product information stored in database"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, unique=True, index=True)
    product_name = Column(String)
    category = Column(String, index=True)
    sub_category = Column(String)
    product_age_days = Column(Integer)
    sales_velocity = Column(Float)
    order_count = Column(Integer)
    return_rate = Column(Float)
    review_score = Column(Float)
    weight_kg = Column(Float)
    dimensions_volume_cm3 = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<Product {self.product_id}>"

class Location(Base):
    """Delivery location information"""
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    state = Column(String, index=True)
    warehouse_distance_km = Column(Float)
    avg_delivery_days = Column(Float)
    delivery_success_rate = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Location {self.city}, {self.state}>"

class Prediction(Base):
    """Stored predictions for tracking and analytics"""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, index=True)
    prediction_timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    deliverability_probability = Column(Float)
    risk_score = Column(Float, index=True)
    prediction_category = Column(String, index=True)
    confidence = Column(Float)
    recommendation = Column(String)
    actual_delivered = Column(Boolean, nullable=True)  # Updated after delivery
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Prediction {self.product_id} - {self.risk_score}>"

class Recommendation(Base):
    """Stored recommendations for products"""
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, index=True)
    recommendation_type = Column(String)  # quality, logistics, timing, etc.
    recommendation_text = Column(Text)
    priority = Column(Integer)  # 1=highest
    estimated_impact = Column(Float)  # Expected improvement percentage
    is_implemented = Column(Boolean, default=False)
    implementation_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Recommendation {self.product_id}>"

class Analytics(Base):
    """Daily aggregated analytics"""
    __tablename__ = "analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True)
    total_predictions = Column(Integer)
    avg_risk_score = Column(Float)
    high_risk_count = Column(Integer)
    delivery_success_rate = Column(Float)
    avg_confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Analytics {self.date}>"

# Database initialization
def init_db():
    """Create all tables in database"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✓ Database tables initialized")
    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}")

def check_db_connection():
    """Check if database connection is working"""
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            logger.info("✓ Database connection successful")
            return True
    except Exception as e:
        logger.error(f"✗ Database connection failed: {e}")
        return False

# Useful queries
def get_product_by_id(db: Session, product_id: str):
    return db.query(Product).filter(Product.product_id == product_id).first()

def get_predictions_by_product(db: Session, product_id: str, limit: int = 10):
    return db.query(Prediction).filter(
        Prediction.product_id == product_id
    ).order_by(Prediction.prediction_timestamp.desc()).limit(limit).all()

def get_high_risk_predictions(db: Session, threshold: float = 70, limit: int = 50):
    return db.query(Prediction).filter(
        Prediction.risk_score >= threshold
    ).order_by(Prediction.risk_score.desc()).limit(limit).all()

def get_daily_analytics(db: Session, date: datetime):
    return db.query(Analytics).filter(Analytics.date == date).first()
