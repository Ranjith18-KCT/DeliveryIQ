"""
DeliverIQ - E-Commerce Deliverability Checker App
Complete Streamlit application with authentication, product browsing, and delivery prediction
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional

# Import custom modules
from auth import login_user, register_user, load_users
from products import PRODUCTS, COIMBATORE_AREAS, get_product_by_id, get_discount_percent
from delivery_logic import (
    predict_deliverability,
    get_delivery_agencies,
    get_nearest_hubs,
    is_electronic_gadget,
    calculate_discount_percent,
    calculate_save_amount
)
from ui_components import (
    render_navbar,
    render_flash_sale_banner,
    render_product_card,
    render_deliverability_checker,
    render_login_card
)

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="DeliverIQ - E-Commerce Deliverability Checker",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== SESSION STATE INITIALIZATION ====================
def initialize_session_state():
    """Initialize all session state variables"""
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "username" not in st.session_state:
        st.session_state["username"] = ""
    if "user_email" not in st.session_state:
        st.session_state["user_email"] = ""
    if "user_location" not in st.session_state:
        st.session_state["user_location"] = ""
    if "location_set" not in st.session_state:
        st.session_state["location_set"] = False
    if "cart" not in st.session_state:
        st.session_state["cart"] = []
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "login"
    if "selected_product" not in st.session_state:
        st.session_state["selected_product"] = None
    if "search_query" not in st.session_state:
        st.session_state["search_query"] = ""
    if "selected_category" not in st.session_state:
        st.session_state["selected_category"] = "All"
    if "price_range" not in st.session_state:
        st.session_state["price_range"] = (0, 200000)

initialize_session_state()

# ==================== LOGIN PAGE ====================
def show_login_page():
    """Display login and registration forms"""
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(
            """
            <div style="
                text-align: center;
                padding: 40px 20px;
                background: linear-gradient(135deg, #FF9900, #2874F0);
                border-radius: 12px;
                color: white;
            ">
                <div style="font-size: 64px; margin-bottom: 20px;">🛒</div>
                <div style="font-size: 32px; font-weight: bold; margin-bottom: 10px;">DeliverIQ</div>
                <div style="font-size: 16px;">Verified Delivery to Your Doorstep</div>
                <div style="margin-top: 20px; font-size: 14px; line-height: 1.6;">
                    ✅ Instant Delivery Status<br>
                    ✅ Best Agencies Network<br>
                    ✅ Transparent Pricing<br>
                    ✅ Real-time Tracking
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        # Tab selection
        tab1, tab2 = st.tabs(["Sign In", "Create Account"])
        
        with tab1:
            st.markdown("### Sign in to continue")
            
            email = st.text_input(
                "Email or User ID",
                placeholder="Enter your email",
                key="login_email"
            )
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_password"
            )
            
            if st.button("🔓 Sign In", use_container_width=True, key="signin_btn"):
                if email and password:
                    success, message, full_name = login_user(email, password)
                    if success:
                        st.session_state["logged_in"] = True
                        st.session_state["username"] = full_name
                        st.session_state["user_email"] = email
                        st.session_state["current_page"] = "location_selection"
                        st.success("✅ " + message)
                        st.rerun()
                    else:
                        st.error("❌ " + message)
                else:
                    st.warning("⚠️ Please enter email and password")
            
            st.divider()
            
            st.markdown(
                """
                <div style="text-align: center; margin-top: 20px;">
                    <a href="#" style="color: #2874F0; text-decoration: none;">
                        🔑 Forgot your password?
                    </a>
                    <br><br>
                    <span style="color: #666; font-size: 12px;">
                        Contact admin to reset password
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with tab2:
            st.markdown("### Create Your Account")
            
            full_name = st.text_input(
                "Full Name",
                placeholder="Your full name",
                key="reg_name"
            )
            reg_email = st.text_input(
                "Email Address",
                placeholder="your.email@example.com",
                key="reg_email"
            )
            phone = st.text_input(
                "Phone Number",
                placeholder="10-digit mobile number",
                key="reg_phone",
                max_chars=10
            )
            reg_password = st.text_input(
                "Password",
                type="password",
                placeholder="Minimum 6 characters",
                key="reg_password"
            )
            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Re-enter your password",
                key="reg_confirm"
            )
            
            if st.button("📝 Create Account", use_container_width=True, key="register_btn"):
                if full_name and reg_email and phone and reg_password:
                    success, message = register_user(
                        reg_email,
                        full_name,
                        phone,
                        reg_password,
                        confirm_password
                    )
                    if success:
                        st.success("✅ " + message)
                        st.info("Now please sign in with your credentials")
                    else:
                        st.error("❌ " + message)
                else:
                    st.warning("⚠️ Please fill in all fields")

# ==================== LOCATION SELECTION PAGE ====================
def show_location_selection_page():
    """Display location selection modal"""
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown(
            f"""
            <div style="
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 24px rgba(0,0,0,0.15);
                padding: 40px;
                text-align: center;
                margin: 50px auto;
            ">
                <div style="font-size: 32px; margin-bottom: 10px;">👋</div>
                <div style="font-size: 24px; font-weight: bold; margin-bottom: 5px;">
                    Welcome, {st.session_state['username']}!
                </div>
                <div style="color: #666; font-size: 14px; margin-bottom: 30px;">
                    Where should we deliver your orders?
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        location = st.selectbox(
            "📍 Select Your Area in Coimbatore",
            COIMBATORE_AREAS,
            key="location_select"
        )
        
        # Manual entry option
        st.markdown("**OR**")
        manual_location = st.text_input(
            "Enter area manually",
            placeholder="Type your area name",
            key="manual_location"
        )
        
        if manual_location:
            location = manual_location
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Confirm Location", use_container_width=True, key="confirm_loc_btn"):
                if location:
                    st.session_state["user_location"] = location
                    st.session_state["location_set"] = True
                    st.session_state["current_page"] = "home"
                    st.success(f"✅ Location set to {location}")
                    st.rerun()
                else:
                    st.warning("⚠️ Please select a location")
        
        with col2:
            if st.button("🚪 Sign Out", use_container_width=True, key="signout_loc_btn"):
                st.session_state["logged_in"] = False
                st.session_state["username"] = ""
                st.session_state["current_page"] = "login"
                st.rerun()

# ==================== HOME PAGE ====================
def show_home_page():
    """Display main home page with product grid"""
    # Navbar with location changer
    col1, col2 = st.columns([1, 10])
    with col1:
        if st.button("↕️", key="change_location_btn", help="Change delivery location"):
            st.session_state["location_set"] = False
            st.rerun()
    with col2:
        st.markdown(f"📍 Delivering to: **{st.session_state['user_location']}**")
    
    st.divider()
    
    # Flash sale banner
    render_flash_sale_banner()
    
    # Search and filters section
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input(
            "🔍 Search for products, brands and more...",
            key="search_input",
            placeholder="Search laptops, mobiles, accessories..."
        )
        st.session_state["search_query"] = search_query
    
    with col2:
        if st.button("🔍 Search", use_container_width=True):
            pass
    
    st.divider()
    
    # Sidebar filters
    with st.sidebar:
        st.markdown("### 🎯 FILTERS")
        
        # Department filter
        departments = ["All", "Laptops", "Mobiles", "Accessories", "Tablets", "Wearables"]
        selected_dept = st.selectbox("Department", departments, key="dept_filter")
        st.session_state["selected_category"] = selected_dept
        
        # Brand filter
        brands = ["All", "Apple", "Samsung", "OnePlus", "Dell", "HP", "Lenovo", "Realme", "Poco"]
        selected_brands = st.multiselect("Brand", brands, default=["All"], key="brand_filter")
        
        # Price range slider
        price_range = st.slider(
            "Price Range (₹)",
            min_value=0,
            max_value=200000,
            value=(0, 200000),
            step=5000,
            key="price_filter"
        )
        st.session_state["price_range"] = price_range
        
        # Rating filter
        min_rating = st.slider("Minimum Rating", 0.0, 5.0, 0.0, 0.1, key="rating_filter")
        
        # Delivery filter
        delivery_types = st.multiselect(
            "Delivery Type",
            ["Express (1-2 days)", "Standard (3-5 days)", "All"],
            default=["All"],
            key="delivery_filter"
        )
        
        st.divider()
        
        if st.button("✅ Apply Filters", use_container_width=True, key="apply_filters_btn"):
            st.success("✅ Filters applied!")
    
    # Filter products based on criteria
    filtered_products = PRODUCTS.copy()
    
    # Filter by search query
    if search_query:
        filtered_products = [
            p for p in filtered_products
            if search_query.lower() in p["name"].lower() or
               search_query.lower() in p["brand"].lower()
        ]
    
    # Filter by category
    if selected_dept != "All":
        filtered_products = [p for p in filtered_products if p["category"] == selected_dept]
    
    # Filter by brand
    if "All" not in selected_brands:
        filtered_products = [p for p in filtered_products if p["brand"] in selected_brands]
    
    # Filter by price range
    filtered_products = [
        p for p in filtered_products
        if price_range[0] <= p["price"] <= price_range[1]
    ]
    
    # Filter by rating
    filtered_products = [p for p in filtered_products if p["rating"] >= min_rating]
    
    # Display product grid
    if filtered_products:
        st.markdown(f"### 🔥 Best Sellers ({len(filtered_products)} products found)")
        
        # Create 3-column grid
        cols = st.columns(3)
        for idx, product in enumerate(filtered_products):
            render_product_card(product, cols[idx % 3])
    else:
        st.info("🔍 No products found. Try different filters!")
    
    # Cart section
    st.divider()
    if st.session_state["cart"]:
        st.markdown(f"### 🛒 Your Cart ({len(st.session_state['cart'])} items)")
        
        cart_col1, cart_col2 = st.columns([3, 1])
        with cart_col1:
            for idx, item in enumerate(st.session_state["cart"]):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"**{item['name'][:40]}...**")
                    st.markdown(f"₹{item['price']:,}")
                with col2:
                    st.markdown(f"({item['rating']}⭐)")
                with col3:
                    if st.button("❌", key=f"remove_{idx}"):
                        st.session_state["cart"].pop(idx)
                        st.rerun()
        
        with cart_col2:
            total = sum(item["price"] for item in st.session_state["cart"])
            st.markdown(f"### ₹{total:,}")
            if st.button("💳 Checkout", use_container_width=True):
                st.success(f"✅ Order placed! Delivering to {st.session_state['user_location']}")
                st.session_state["cart"] = []
                st.rerun()

# ==================== PRODUCT DETAIL PAGE ====================
def show_product_detail_page():
    """Display detailed product page with deliverability checker"""
    if not st.session_state["selected_product"]:
        st.warning("No product selected")
        if st.button("← Back to Home"):
            st.session_state["current_page"] = "home"
            st.rerun()
        return
    
    product = st.session_state["selected_product"]
    discount = calculate_discount_percent(product)
    
    # Breadcrumb
    if st.button("← Back to Home"):
        st.session_state["current_page"] = "home"
        st.rerun()
    
    st.markdown(f"**Home > {product['category']} > {product['name'][:30]}...**")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Product Images")
        st.image(product["image"], width=300)
        st.markdown("*Thumbnail images would appear here*")
    
    with col2:
        st.markdown(f"### {product['name']}")
        st.markdown(f"**Brand:** {product['brand']}")
        
        # Rating
        st.markdown(
            f"⭐ {product['rating']} ({product['reviews']:,} ratings)"
        )
        
        # Price section
        st.markdown(f"## ₹{product['price']:,}")
        st.markdown(f"~~₹{product['original_price']:,}~~ | **{discount}% off** | {calculate_save_amount(product)}")
        
        # EMI info
        if product.get('emi'):
            st.success(f"✅ No Cost EMI from {product['emi']}")
        
        # Highlights
        st.markdown("### ✨ Highlights")
        for highlight in product["highlights"]:
            st.markdown(f"• {highlight}")
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🛒 Add to Cart", use_container_width=True):
                st.session_state["cart"].append(product)
                st.success(f"✅ Added to cart!")
        with col2:
            if st.button("💳 Buy Now", use_container_width=True):
                st.session_state["cart"].append(product)
                st.success(f"✅ Proceeding to checkout...")
    
    st.divider()
    
    # Deliverability Checker
    render_deliverability_checker(product, st.session_state["user_location"])
    
    st.divider()
    
    # Customer Reviews Section
    st.markdown("### 👥 Customer Reviews")
    st.markdown(f"Average Rating: ⭐ {product['rating']}/5 ({product['reviews']:,} reviews)")
    
    # Sample reviews
    reviews = [
        {"author": "John Doe", "rating": 5, "text": "Excellent product! Fast delivery and great quality."},
        {"author": "Jane Smith", "rating": 4, "text": "Good value for money. Minor packaging issue but resolved quickly."},
        {"author": "Raj Kumar", "rating": 5, "text": "Best purchase! Verified delivery as promised."}
    ]
    
    for review in reviews:
        st.markdown(f"**{review['author']}** - ⭐ {review['rating']}/5")
        st.markdown(f"*{review['text']}*")
        st.divider()

# ==================== NAVIGATION LOGIC ====================
def main():
    """Main app routing logic"""
    
    # Check authentication
    if not st.session_state["logged_in"]:
        show_login_page()
    elif not st.session_state["location_set"]:
        show_location_selection_page()
    elif st.session_state["current_page"] == "product_detail":
        # Top navbar for product detail page
        col1, col2, col3 = st.columns([1, 5, 1])
        with col1:
            st.markdown("🛒 **DeliverIQ**")
        with col2:
            col_change, col_info = st.columns([1, 4])
            with col_change:
                if st.button("📍 " + st.session_state["user_location"], key="change_loc_detail"):
                    st.session_state["location_set"] = False
                    st.rerun()
            with col_info:
                st.markdown(f"👤 {st.session_state['username']} | 🛒 Cart: {len(st.session_state['cart'])}")
        with col3:
            if st.button("🚪 Sign Out", key="signout_detail"):
                st.session_state["logged_in"] = False
                st.rerun()
        
        st.divider()
        show_product_detail_page()
    else:
        # Top navbar for home page
        col1, col2, col3 = st.columns([1, 5, 1])
        with col1:
            st.markdown("🛒 **DeliverIQ**")
        with col2:
            col_change, col_info = st.columns([1, 4])
            with col_change:
                if st.button("📍 " + st.session_state["user_location"], key="change_loc_home"):
                    st.session_state["location_set"] = False
                    st.rerun()
            with col_info:
                st.markdown(f"👤 {st.session_state['username']} | 🛒 Cart: {len(st.session_state['cart'])}")
        with col3:
            if st.button("🚪 Sign Out", key="signout_home"):
                st.session_state["logged_in"] = False
                st.rerun()
        
        st.divider()
        show_home_page()

if __name__ == "__main__":
    main()
