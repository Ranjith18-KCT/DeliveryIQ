"""
Product Data Module
Defines all e-commerce products with detailed information
"""

PRODUCTS = [
    {
        "id": 1,
        "name": "Apple MacBook Air M2 13-inch",
        "brand": "Apple",
        "category": "Laptops",
        "price": 89999,
        "original_price": 114900,
        "rating": 4.7,
        "reviews": 8432,
        "image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400",
        "exchange": True,
        "emi": "₹7,500/month",
        "highlights": [
            "Apple M2 Chip with 8-core CPU and 10-core GPU",
            "13.6-inch Liquid Retina Display",
            "8GB Unified Memory | 512GB SSD Storage",
            "Up to 18 hours battery life"
        ]
    },
    {
        "id": 2,
        "name": "Samsung Galaxy S24 Ultra 5G 256GB",
        "brand": "Samsung",
        "category": "Mobiles",
        "price": 109999,
        "original_price": 134999,
        "rating": 4.6,
        "reviews": 21043,
        "image": "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400",
        "exchange": True,
        "emi": "₹9,167/month",
        "highlights": [
            "6.8-inch Dynamic AMOLED 2X Display",
            "Snapdragon 8 Gen 3 Processor",
            "50MP + 50MP + 48MP + 10MP Quad Camera",
            "5000mAh Battery with 65W Fast Charging"
        ]
    },
    {
        "id": 3,
        "name": "OnePlus Nord CE 4 5G 128GB",
        "brand": "OnePlus",
        "category": "Mobiles",
        "price": 24999,
        "original_price": 29999,
        "rating": 4.3,
        "reviews": 6721,
        "image": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=400",
        "exchange": True,
        "emi": "₹2,083/month",
        "highlights": [
            "6.7-inch AMOLED Display with 120Hz refresh rate",
            "Snapdragon 7 Gen 1 Accelerated Processor",
            "50MP Main Camera + 8MP Ultra-Wide",
            "5500mAh Battery with 100W Fast Charging"
        ]
    },
    {
        "id": 4,
        "name": "Dell Inspiron 15 Intel i5 16GB RAM",
        "brand": "Dell",
        "category": "Laptops",
        "price": 57490,
        "original_price": 75000,
        "rating": 4.4,
        "reviews": 3290,
        "image": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=400",
        "exchange": False,
        "emi": "₹4,791/month",
        "highlights": [
            "Intel Core i5-12450H Processor",
            "15.6-inch FHD (1920x1200) Anti-glare Display",
            "16GB DDR4 RAM | 512GB SSD Storage",
            "NVIDIA GeForce MX450 Graphics"
        ]
    },
    {
        "id": 5,
        "name": "HP Pavilion Gaming Laptop RTX 3050",
        "brand": "HP",
        "category": "Laptops",
        "price": 67999,
        "original_price": 89999,
        "rating": 4.5,
        "reviews": 5102,
        "image": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=400",
        "exchange": True,
        "emi": "₹5,667/month",
        "highlights": [
            "Intel Core i7-12700H (14-core) Processor",
            "16-inch FHD (1920x1200) IPS Display",
            "16GB DDR4 RAM | 512GB SSD Storage",
            "NVIDIA GeForce RTX 3050 4GB Graphics"
        ]
    },
    {
        "id": 6,
        "name": "boAt Rockerz 550 Bluetooth Headphone",
        "brand": "boAt",
        "category": "Accessories",
        "price": 1299,
        "original_price": 3990,
        "rating": 4.1,
        "reviews": 98231,
        "image": "https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=400",
        "exchange": False,
        "emi": None,
        "highlights": [
            "Active Noise Cancellation (ANC)",
            "40 hours battery life",
            "ASAP Charge: 10 mins = 10 hours playtime",
            "Premium build with dual pairing"
        ]
    },
    {
        "id": 7,
        "name": "Anker 65W GaN USB-C Charger",
        "brand": "Anker",
        "category": "Accessories",
        "price": 2499,
        "original_price": 3499,
        "rating": 4.6,
        "reviews": 11203,
        "image": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=400",
        "exchange": False,
        "emi": None,
        "highlights": [
            "GaN Technology - Compact & Lightweight",
            "65W Total Power Delivery",
            "Supports Multiple Devices Simultaneously",
            "Foldable Plug for Easy Portability"
        ]
    },
    {
        "id": 8,
        "name": "Lenovo IdeaPad Slim 5 AMD Ryzen 5",
        "brand": "Lenovo",
        "category": "Laptops",
        "price": 52999,
        "original_price": 69999,
        "rating": 4.3,
        "reviews": 4871,
        "image": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=400",
        "exchange": True,
        "emi": "₹4,417/month",
        "highlights": [
            "AMD Ryzen 5 5600H Processor",
            "15.6-inch FHD IPS Display with 300 nits",
            "16GB DDR4 RAM | 512GB SSD Storage",
            "Radeon Graphics with 8GB VRAM"
        ]
    },
    {
        "id": 9,
        "name": "Redmi Note 13 Pro 5G 256GB",
        "brand": "Redmi",
        "category": "Mobiles",
        "price": 23999,
        "original_price": 29999,
        "rating": 4.4,
        "reviews": 43210,
        "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400",
        "exchange": True,
        "emi": "₹2,000/month",
        "highlights": [
            "6.67-inch AMOLED Display with 120Hz refresh",
            "Snapdragon 7 Gen 1 Processor",
            "50MP + 8MP Dual Camera | 16MP Selfie",
            "5000mAh Battery with 67W Fast Charging"
        ]
    },
    {
        "id": 10,
        "name": "MI Power Bank 3i 20000mAh",
        "brand": "Xiaomi",
        "category": "Accessories",
        "price": 1299,
        "original_price": 1999,
        "rating": 4.3,
        "reviews": 87654,
        "image": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=400",
        "exchange": False,
        "emi": None,
        "highlights": [
            "20000mAh High Capacity",
            "Dual USB Output Ports + USB-C Input",
            "Support for 18W Fast Charging",
            "LED Display with Battery Indicator"
        ]
    },
    {
        "id": 11,
        "name": "Sony PlayStation 5 Console",
        "brand": "Sony",
        "category": "Gaming",
        "price": 49990,
        "original_price": 54990,
        "rating": 4.9,
        "reviews": 15420,
        "image": "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=400",
        "exchange": False,
        "emi": "₹4,166/month",
        "highlights": [
            "Ultra-High Speed SSD",
            "Ray Tracing Technology",
            "4K-TV Gaming up to 120fps",
            "Tempest 3D AudioTech"
        ]
    },
    {
        "id": 12,
        "name": "Apple iPad Air (5th Gen)",
        "brand": "Apple",
        "category": "Tablets",
        "price": 59900,
        "original_price": 69900,
        "rating": 4.8,
        "reviews": 8940,
        "image": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400",
        "exchange": True,
        "emi": "₹4,992/month",
        "highlights": [
            "10.9-inch Liquid Retina display",
            "Apple M1 chip",
            "12MP Ultra Wide front camera",
            "Works with Magic Keyboard"
        ]
    },
    {
        "id": 13,
        "name": "Samsung Odyssey G5 27-inch Monitor",
        "brand": "Samsung",
        "category": "Accessories",
        "price": 22999,
        "original_price": 35000,
        "rating": 4.5,
        "reviews": 3210,
        "image": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400",
        "exchange": False,
        "emi": "₹1,917/month",
        "highlights": [
            "27-inch WQHD (2560x1440) Curved Panel",
            "144Hz Refresh Rate",
            "1ms Response Time",
            "AMD FreeSync Premium"
        ]
    },
    {
        "id": 14,
        "name": "Sony WH-1000XM5 Wireless ANC Headphones",
        "brand": "Sony",
        "category": "Accessories",
        "price": 29990,
        "original_price": 34990,
        "rating": 4.7,
        "reviews": 11200,
        "image": "https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=400",
        "exchange": False,
        "emi": "₹2,499/month",
        "highlights": [
            "Industry-Leading Noise Cancellation",
            "Up to 30 Hours Battery Life",
            "Multipoint Connection",
            "Crystal Clear Hands-Free Calling"
        ]
    },
    {
        "id": 15,
        "name": "Apple Watch Series 9 (GPS, 45mm)",
        "brand": "Apple",
        "category": "Wearables",
        "price": 44900,
        "original_price": 44900,
        "rating": 4.8,
        "reviews": 5600,
        "image": "https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=400",
        "exchange": True,
        "emi": "₹3,742/month",
        "highlights": [
            "S9 SiP with Double Tap Gesture",
            "Always-On Retina Display",
            "Blood Oxygen & ECG Apps",
            "Crash Detection & Fall Detection"
        ]
    },
    {
        "id": 16,
        "name": "Canon EOS R5 Mirrorless Camera",
        "brand": "Canon",
        "category": "Cameras",
        "price": 319990,
        "original_price": 339990,
        "rating": 4.9,
        "reviews": 1250,
        "image": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400",
        "exchange": False,
        "emi": "₹26,666/month",
        "highlights": [
            "45MP Full-Frame CMOS Sensor",
            "8K Video Recording",
            "In-Body Image Stabilizer",
            "Dual Pixel CMOS AF II"
        ]
    }
]

COIMBATORE_AREAS = [
    "KCT Campus (Saravanampatti)",
    "RS Puram",
    "Gandhipuram",
    "Saibaba Colony",
    "Peelamedu",
    "Singanallur",
    "Vadavalli",
    "Kuniyamuthur",
    "Ganapathy",
    "Kovaipudur",
    "Ondipudur",
    "Hopes College",
    "Race Course",
    "Town Hall",
    "Ukkadam",
    "Sulur",
    "Kinathukadavu",
    "Mettupalayam",
    "Pollachi",
    "Valparai",
    "Annur",
    "Palladam",
    "Tirupur Road",
    "Podanur",
    "Thondamuthur",
    "Karamadai"
]

def get_product_by_id(product_id: int) -> dict:
    """Get product details by ID"""
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product
    return None

def get_discount_percent(product: dict) -> int:
    """Calculate discount percentage"""
    if product["original_price"] > 0:
        discount = ((product["original_price"] - product["price"]) / product["original_price"]) * 100
        return int(discount)
    return 0
