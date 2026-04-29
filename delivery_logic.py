"""
Delivery Logic Module
Handles deliverability predictions, agency info, and delivery calculations
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path

def is_electronic_gadget(product_name: str) -> bool:
    """Check if product is an electronic gadget"""
    laptop_keywords = [
        "laptop", "notebook", "macbook", "chromebook", "ultrabook",
        "laptop charger", "laptop bag", "cooling pad", "docking station",
        "laptop stand", "laptop sleeve"
    ]
    mobile_keywords = [
        "mobile", "smartphone", "iphone", "android", "oneplus",
        "samsung", "realme", "redmi", "poco", "phone case",
        "screen protector", "charger", "earphones", "tws",
        "power bank", "otg", "phone holder", "selfie stick",
        "headphone", "earbuds", "galaxy"
    ]
    
    name_lower = product_name.lower()
    return any(k in name_lower for k in laptop_keywords + mobile_keywords)

def predict_deliverability(product: Dict, location: str) -> Dict:
    """
    Predict deliverability to a given location
    
    Returns:
    {
        "deliverable": bool,
        "confidence": float (0.0-1.0),
        "predicted_days": int,
        "delivery_type": str,
        "arrival_date": str,
        "color": str
    }
    """
    # For now, use simulation mode
    # In production, this would load and use the actual DNN model
    
    # Basic rules for Coimbatore areas
    coimbatore_areas = [
        "KCT Campus (Saravanampatti)", "RS Puram", "Gandhipuram", "Saibaba Colony",
        "Peelamedu", "Singanallur", "Vadavalli", "Kuniyamuthur", "Ganapathy",
        "Kovaipudur", "Ondipudur", "Hopes College", "Race Course", "Town Hall",
        "Ukkadam", "Sulur", "Kinathukadavu", "Mettupalayam", "Pollachi",
        "Valparai", "Annur", "Palladam", "Tirupur Road", "Podanur",
        "Thondamuthur", "Karamadai"
    ]
    
    is_gadget = is_electronic_gadget(product.get("name", ""))
    is_valid_location = location in coimbatore_areas
    
    # Determine deliverability
    if not is_valid_location:
        return {
            "deliverable": False,
            "confidence": 0.15,
            "predicted_days": None,
            "delivery_type": "Unknown",
            "arrival_date": "Unknown",
            "color": "#cc0000"
        }
    
    if not is_gadget:
        # Non-gadget items have lower confidence
        confidence = random.uniform(0.70, 0.85)
        predicted_days = random.randint(4, 9)
    else:
        # Electronic gadgets in Coimbatore have high confidence
        confidence = random.uniform(0.94, 0.99)
        predicted_days = random.randint(1, 7)
    
    # Determine delivery type based on predicted days
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
    
    # Calculate arrival date
    arrival_datetime = datetime.today() + timedelta(days=predicted_days)
    arrival_date = arrival_datetime.strftime("%A, %d %B %Y")
    
    return {
        "deliverable": True,
        "confidence": round(confidence * 100, 1),
        "predicted_days": predicted_days,
        "delivery_type": delivery_type,
        "arrival_date": arrival_date,
        "color": color
    }

def get_delivery_agencies() -> List[Dict]:
    """Get list of delivery agencies in Coimbatore"""
    return [
        {
            "name": "Blue Dart",
            "hub": "Gandhipuram",
            "eta_days": 1,
            "contact": "1860-233-1234",
            "website": "https://www.bluedart.com",
            "latitude": 11.0046,
            "longitude": 76.9707
        },
        {
            "name": "Amazon Logistics",
            "hub": "Sulur",
            "eta_days": 1,
            "contact": "1800-419-7355",
            "website": "https://www.amazon.in",
            "latitude": 11.0022,
            "longitude": 77.0053
        },
        {
            "name": "Delhivery",
            "hub": "Peelamedu",
            "eta_days": 2,
            "contact": "1800-208-1888",
            "website": "https://www.delhivery.com",
            "latitude": 11.0168,
            "longitude": 76.9558
        },
        {
            "name": "Xpressbees",
            "hub": "Peelamedu",
            "eta_days": 2,
            "contact": "1800-266-8666",
            "website": "https://www.xpressbees.com",
            "latitude": 11.0168,
            "longitude": 76.9558
        },
        {
            "name": "Shadowfax",
            "hub": "Ukkadam",
            "eta_days": 2,
            "contact": "App only",
            "website": "https://shadowfax.in",
            "latitude": 11.0106,
            "longitude": 76.9486
        },
        {
            "name": "DTDC",
            "hub": "RS Puram",
            "eta_days": 3,
            "contact": "1800-102-3817",
            "website": "https://www.dtdc.in",
            "latitude": 11.0034,
            "longitude": 76.9635
        },
        {
            "name": "Ecom Express",
            "hub": "Singanallur",
            "eta_days": 3,
            "contact": "1800-103-7887",
            "website": "https://www.ecomexpress.in",
            "latitude": 10.9871,
            "longitude": 76.9487
        }
    ]

def get_nearest_hubs(user_area: str, agencies: List[Dict]) -> List[Dict]:
    """
    Get delivery agencies sorted by proximity to user area
    Returns agencies sorted by distance/ETA
    """
    hub_zones = {
        "Peelamedu": [
            "KCT Campus (Saravanampatti)", "Peelamedu", "Hopes College",
            "Race Course", "Ondipudur"
        ],
        "Gandhipuram": [
            "Gandhipuram", "RS Puram", "Town Hall", "Saibaba Colony", "Ganapathy"
        ],
        "Singanallur": [
            "Singanallur", "Ukkadam", "Podanur", "Tirupur Road", "Palladam"
        ],
        "Sulur": ["Sulur", "Annur", "Karamadai", "Mettupalayam"],
        "RS Puram": [
            "RS Puram", "Vadavalli", "Kovaipudur", "Kuniyamuthur", "Thondamuthur"
        ],
        "Ukkadam": ["Ukkadam", "Kinathukadavu", "Pollachi", "Valparai"]
    }
    
    # Find which hub zone the user's area belongs to
    nearest_hub = None
    for hub, areas in hub_zones.items():
        if user_area in areas:
            nearest_hub = hub
            break
    
    # Prioritize agencies in the nearest hub
    if nearest_hub:
        priority_agencies = [a for a in agencies if a["hub"] == nearest_hub]
        rest_agencies = [a for a in agencies if a["hub"] != nearest_hub]
        # Sort each group by ETA
        sorted_priority = sorted(priority_agencies, key=lambda x: x["eta_days"])
        sorted_rest = sorted(rest_agencies, key=lambda x: x["eta_days"])
        return sorted_priority + sorted_rest
    
    # If user area not recognized, sort all by ETA
    return sorted(agencies, key=lambda x: x["eta_days"])

def calculate_save_amount(product: Dict) -> str:
    """Calculate amount saved from original price"""
    saving = product["original_price"] - product["price"]
    return f"Save ₹{saving:,}"

def calculate_discount_percent(product: Dict) -> int:
    """Calculate discount percentage"""
    if product["original_price"] > 0:
        discount = ((product["original_price"] - product["price"]) / product["original_price"]) * 100
        return int(discount)
    return 0
