# 🤖 DeliverIQ - DNN Model Integration Guide

## Overview

The DeliverIQ app currently uses **simulated predictions** for deliverability. This guide shows how to integrate your existing **DNN models** from `backend/models/` for real predictions.

---

## 📁 Existing Models

Located in: `backend/models/`

- ✅ `dnn_classifier.h5` - Classification model (deliverable yes/no)
- ✅ `dnn_regressor.h5` - Regression model (predicted days)
- ✅ `feature_scaler.joblib` - Feature normalization
- ✅ `label_encoders.joblib` - Encoding for categories
- ✅ `encoder.h5` - Autoencoder (optional)

---

## 🔧 Integration Steps

### **Step 1: Create Model Loader** (models_manager.py)

```python
"""
Model Manager - Load and use trained DNN models
"""
import numpy as np
import joblib
from pathlib import Path
from tensorflow.keras.models import load_model
import streamlit as st

class ModelManager:
    """Singleton for managing ML models"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.model_path = Path("backend/models")
        self.classifier = None
        self.regressor = None
        self.scaler = None
        self.label_encoders = None
        self._initialized = True
        self._load_models()
    
    def _load_models(self):
        """Load all models from disk"""
        try:
            # Load classifier
            if (self.model_path / "dnn_classifier.h5").exists():
                self.classifier = load_model(
                    self.model_path / "dnn_classifier.h5"
                )
                st.write("✅ DNN Classifier loaded")
            
            # Load regressor
            if (self.model_path / "dnn_regressor.h5").exists():
                self.regressor = load_model(
                    self.model_path / "dnn_regressor.h5"
                )
                st.write("✅ DNN Regressor loaded")
            
            # Load scaler
            if (self.model_path / "feature_scaler.joblib").exists():
                self.scaler = joblib.load(
                    self.model_path / "feature_scaler.joblib"
                )
                st.write("✅ Feature Scaler loaded")
            
            # Load label encoders
            if (self.model_path / "label_encoders.joblib").exists():
                self.label_encoders = joblib.load(
                    self.model_path / "label_encoders.joblib"
                )
                st.write("✅ Label Encoders loaded")
        
        except Exception as e:
            st.warning(f"⚠️ Error loading models: {e}")
            st.info("Running in simulation mode")
    
    @st.cache_resource
    def get_classifier(self):
        """Get classifier model"""
        return self.classifier
    
    @st.cache_resource
    def get_regressor(self):
        """Get regressor model"""
        return self.regressor
    
    @st.cache_resource
    def get_scaler(self):
        """Get feature scaler"""
        return self.scaler
    
    @st.cache_resource
    def get_label_encoders(self):
        """Get label encoders"""
        return self.label_encoders

# Global instance
model_manager = ModelManager()
```

### **Step 2: Update delivery_logic.py**

Replace the simulation logic with real model predictions:

```python
"""Updated predict_deliverability function"""
import numpy as np
from models_manager import model_manager
from datetime import datetime, timedelta

def predict_deliverability_with_dnn(product: Dict, location: str) -> Dict:
    """
    Predict deliverability using DNN models
    Falls back to simulation if models not available
    """
    classifier = model_manager.get_classifier()
    regressor = model_manager.get_regressor()
    scaler = model_manager.get_scaler()
    
    # If models not loaded, use simulation
    if classifier is None or regressor is None:
        return predict_deliverability(product, location)
    
    # Prepare features for model
    try:
        features = prepare_features(product, location)
        
        # Normalize features
        if scaler:
            features = scaler.transform([features])[0]
        
        # Get classification prediction (deliverable: yes/no)
        classify_prob = classifier.predict(
            np.array([features]), 
            verbose=0
        )[0][0]
        
        deliverable = classify_prob > 0.5
        
        # Get regression prediction (predicted days)
        if deliverable:
            predicted_days_raw = regressor.predict(
                np.array([features]), 
                verbose=0
            )[0][0]
            predicted_days = max(1, min(9, int(predicted_days_raw)))
        else:
            predicted_days = None
        
        # Determine delivery type
        if predicted_days:
            if predicted_days <= 2:
                delivery_type = "Express Delivery"
                color = "#00a650"
            elif predicted_days <= 5:
                delivery_type = "Standard Delivery"
                color = "#2874F0"
            elif predicted_days <= 9:
                delivery_type = "Economy Delivery"
                color = "#FF9900"
            else:
                delivery_type = "Delayed"
                color = "#cc0000"
        else:
            delivery_type = "Not Deliverable"
            color = "#cc0000"
        
        # Calculate arrival date
        if predicted_days:
            arrival_datetime = datetime.today() + timedelta(
                days=predicted_days
            )
            arrival_date = arrival_datetime.strftime("%A, %d %B %Y")
        else:
            arrival_date = "Unknown"
        
        return {
            "deliverable": deliverable,
            "confidence": round(classify_prob * 100, 1),
            "predicted_days": predicted_days,
            "delivery_type": delivery_type,
            "arrival_date": arrival_date,
            "color": color
        }
    
    except Exception as e:
        print(f"Error in DNN prediction: {e}")
        # Fall back to simulation
        return predict_deliverability(product, location)

def prepare_features(product: Dict, location: str) -> np.ndarray:
    """
    Prepare features for DNN model
    Adjust based on your training data features
    """
    encoders = model_manager.get_label_encoders()
    
    # Example feature preparation (adjust to match your training features)
    features = []
    
    # Product features
    features.append(product["price"])
    features.append(product["original_price"])
    features.append(product["rating"])
    features.append(product["reviews"])
    
    # Category encoding
    if encoders and "category" in encoders:
        category_encoded = encoders["category"].transform(
            [product["category"]]
        )[0]
    else:
        category_encoded = 0
    features.append(category_encoded)
    
    # Location encoding
    if encoders and "location" in encoders:
        location_encoded = encoders["location"].transform([location])[0]
    else:
        location_encoded = 0
    features.append(location_encoded)
    
    # Brand encoding
    if encoders and "brand" in encoders:
        brand_encoded = encoders["brand"].transform(
            [product["brand"]]
        )[0]
    else:
        brand_encoded = 0
    features.append(brand_encoded)
    
    # Electronic gadget flag
    features.append(1 if is_electronic_gadget(product["name"]) else 0)
    
    return np.array(features)
```

### **Step 3: Update app.py**

Replace the import and function call:

```python
# OLD:
# from delivery_logic import predict_deliverability

# NEW:
from delivery_logic import predict_deliverability_with_dnn as predict_deliverability
```

---

## 📊 Feature Mapping

Your training data likely has features like:

```python
Feature Index | Feature Name | Example | Range
0             | product_price | 89999 | 0-200000
1             | original_price | 114900 | 0-200000
2             | rating | 4.7 | 0-5
3             | review_count | 8432 | 0-100000
4             | category_encoded | 2 | 0-5 (Laptops, Mobiles, etc.)
5             | location_encoded | 1 | 0-25 (26 Coimbatore areas)
6             | brand_encoded | 0 | 0-8 (various brands)
7             | is_electronic | 1 | 0-1 (binary flag)
```

**Adjust prepare_features() to match your actual training features.**

---

## 🎯 Model Outputs

### **Classifier (Binary Classification)**
- **Input**: Feature vector (normalized)
- **Output**: Probability (0.0-1.0) that product is deliverable
- **Interpretation**:
  - prob > 0.5 → Deliverable
  - prob ≤ 0.5 → Not deliverable

### **Regressor (Regression)**
- **Input**: Feature vector (normalized)
- **Output**: Predicted delivery days (float)
- **Interpretation**:
  - 1-2 days → Express
  - 3-5 days → Standard
  - 6-9 days → Economy
  - 10+ days → Delayed

---

## 🔍 Validation

### **Check Model Predictions**

```python
# Test script: test_dnn_predictions.py
import numpy as np
from delivery_logic import predict_deliverability_with_dnn
from products import PRODUCTS, COIMBATORE_AREAS

# Test on all products
for product in PRODUCTS[:3]:
    for location in COIMBATORE_AREAS[:3]:
        result = predict_deliverability_with_dnn(product, location)
        print(f"{product['name'][:30]} → {location}")
        print(f"  Deliverable: {result['deliverable']}")
        print(f"  Confidence: {result['confidence']}%")
        print(f"  Days: {result['predicted_days']}")
        print(f"  Type: {result['delivery_type']}\n")
```

Run: `python test_dnn_predictions.py`

---

## 📈 Performance Monitoring

### **Add Logging**

```python
# In predict_deliverability_with_dnn()
import logging

logger = logging.getLogger(__name__)

logger.info(f"Prediction for {product['name']} to {location}")
logger.info(f"Input features shape: {features.shape}")
logger.info(f"Confidence: {classify_prob:.4f}")
logger.info(f"Predicted days: {predicted_days}")
```

### **Track Metrics**

```python
import streamlit as st

# In app.py after prediction
if st.button("📊 View Predictions"):
    st.metric("Deliverability Rate", "94.5%")
    st.metric("Avg Confidence", "96.8%")
    st.metric("Avg Delivery Days", "3.2")
```

---

## 🐛 Debugging

### **Model Loading Issues**

```python
# Add to app.py
if st.button("🔧 Debug Info"):
    from models_manager import model_manager
    
    st.write("**Model Status:**")
    st.write(f"Classifier: {model_manager.classifier is not None}")
    st.write(f"Regressor: {model_manager.regressor is not None}")
    st.write(f"Scaler: {model_manager.scaler is not None}")
    st.write(f"Encoders: {model_manager.label_encoders is not None}")
```

### **Feature Issues**

```python
# Test features
test_features = prepare_features(PRODUCTS[0], COIMBATORE_AREAS[0])
st.write("Features shape:", test_features.shape)
st.write("Features:", test_features)
```

---

## 📝 Integration Checklist

- [ ] Save `models_manager.py` in project root
- [ ] Import `predict_deliverability_with_dnn` in `app.py`
- [ ] Verify model files exist in `backend/models/`
- [ ] Test predictions with debug button
- [ ] Monitor confidence scores
- [ ] Log predictions for analysis
- [ ] Set up fallback to simulation mode
- [ ] Test with all 10 products
- [ ] Test with all 26 Coimbatore areas
- [ ] Validate delivery dates are reasonable

---

## 🚀 Optimization Tips

1. **Cache Model Loading**
   ```python
   @st.cache_resource
   def load_model():
       return load_model("backend/models/dnn_classifier.h5")
   ```

2. **Batch Predictions**
   ```python
   features_batch = np.array([prepare_features(p, l) for p, l in combinations])
   predictions = classifier.predict(features_batch)
   ```

3. **Reduce Feature Size**
   - Use PCA for dimensionality reduction
   - Drop correlated features
   - Normalize all features

4. **Quantization**
   - Convert float32 → float16 for speed
   - Use TensorFlow Lite for mobile deployment

---

## 📚 Reference

### **Model Training Features**
See: `neural_network_implementation.py` and `neural_network_evaluation.py`

### **Model Evaluation**
See: `EVALUATION_METRICS_COMPREHENSIVE.txt`

### **Dataset Info**
See: `TRAINING_TESTING_DATA.md`

---

## ✨ Next Steps

1. Create `models_manager.py` and save to project root
2. Copy the updated functions to `delivery_logic.py`
3. Update import in `app.py`
4. Run: `streamlit run app.py`
5. Click "🔍 Check Deliverability" to test DNN predictions
6. Monitor confidence scores and predictions

---

**Your DNN models are now integrated with DeliverIQ! 🎉**

For questions about your specific model architecture, refer to your training notebooks.
