-- PostgreSQL Database Schema for Non-Deliverable Prediction System
-- Create this database before running the backend application

-- Create database (run separately first)
-- CREATE DATABASE ecommerce_db;

-- Create tables
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(50) UNIQUE NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    sub_category VARCHAR(100),
    product_age_days INTEGER,
    sales_velocity FLOAT,
    order_count INTEGER,
    return_rate FLOAT,
    review_score FLOAT,
    weight_kg FLOAT,
    dimensions_volume_cm3 FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS locations (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    warehouse_distance_km FLOAT,
    avg_delivery_days FLOAT,
    delivery_success_rate FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    prediction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deliverability_probability FLOAT NOT NULL,
    risk_score FLOAT NOT NULL,
    prediction_category VARCHAR(50) NOT NULL,
    confidence FLOAT NOT NULL,
    recommendation TEXT,
    actual_delivered BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS recommendations (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    recommendation_type VARCHAR(50) NOT NULL,
    recommendation_text TEXT NOT NULL,
    priority INTEGER,
    estimated_impact FLOAT,
    is_implemented BOOLEAN DEFAULT FALSE,
    implementation_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS analytics (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    total_predictions INTEGER,
    avg_risk_score FLOAT,
    high_risk_count INTEGER,
    delivery_success_rate FLOAT,
    avg_confidence FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_active ON products(is_active);
CREATE INDEX idx_locations_city_state ON locations(city, state);
CREATE INDEX idx_predictions_product_id ON predictions(product_id);
CREATE INDEX idx_predictions_timestamp ON predictions(prediction_timestamp);
CREATE INDEX idx_predictions_risk_score ON predictions(risk_score DESC);
CREATE INDEX idx_predictions_category ON predictions(prediction_category);
CREATE INDEX idx_recommendations_product_id ON recommendations(product_id);
CREATE INDEX idx_recommendations_priority ON recommendations(priority);
CREATE INDEX idx_analytics_date ON analytics(date DESC);

-- Create view for high-risk products
CREATE VIEW high_risk_products AS
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    AVG(pred.risk_score) as avg_risk_score,
    COUNT(*) as prediction_count,
    MAX(pred.prediction_timestamp) as last_prediction
FROM products p
JOIN predictions pred ON p.product_id = pred.product_id
WHERE pred.risk_score >= 70
GROUP BY p.product_id, p.product_name, p.category
ORDER BY avg_risk_score DESC;

-- Create view for delivery analytics by category
CREATE VIEW category_analytics AS
SELECT 
    p.category,
    COUNT(DISTINCT p.product_id) as total_products,
    AVG(pred.risk_score) as avg_risk_score,
    AVG(pred.deliverability_probability) as avg_deliverability,
    COUNT(pred.id) as total_predictions,
    SUM(CASE WHEN pred.actual_delivered = TRUE THEN 1 ELSE 0 END) as delivered_count
FROM products p
LEFT JOIN predictions pred ON p.product_id = pred.product_id
WHERE p.is_active = TRUE
GROUP BY p.category
ORDER BY avg_risk_score DESC;

-- Insert sample data (optional)
INSERT INTO locations (city, state, warehouse_distance_km, avg_delivery_days, delivery_success_rate) VALUES
('Mumbai', 'Maharashtra', 0, 1.5, 0.98),
('Delhi', 'Delhi', 120, 2.5, 0.96),
('Bangalore', 'Karnataka', 80, 2.0, 0.97),
('Kolkata', 'West Bengal', 450, 4.0, 0.91),
('Chennai', 'Tamil Nadu', 520, 3.5, 0.94),
('Hyderabad', 'Telangana', 250, 3.0, 0.93)
ON CONFLICT DO NOTHING;

-- Grant permissions (modify user as needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_app_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_app_user;
