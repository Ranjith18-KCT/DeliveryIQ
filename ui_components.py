"""
UI Components Module
Reusable Streamlit UI components for the DeliverIQ app
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from typing import List, Dict
from delivery_logic import calculate_discount_percent, calculate_save_amount

def render_navbar(username: str, user_location: str, cart_count: int) -> None:
    """Render top navigation bar"""
    st.markdown(
        f"""
        <div style="
            background-color: #0F1111;
            padding: 12px 20px;
            position: sticky;
            top: 0;
            z-index: 1000;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 4px solid;
            border-image: linear-gradient(90deg, #FF9900, #2874F0) 1;
            color: white;
            font-size: 14px;
        ">
            <div style="display: flex; align-items: center; gap: 20px;">
                <span style="font-size: 22px; font-weight: bold;">🛒 DeliverIQ</span>
                <span style="border-left: 1px solid #666; padding-left: 20px;">
                    📍 Delivering to <b>{user_location}</b>
                </span>
            </div>
            <div style="display: flex; align-items: center; gap: 20px;">
                <span>👤 Hello, <b>{username}</b></span>
                <span style="border: 1px solid #FF9900; padding: 4px 8px; border-radius: 4px;">
                    🛒 Cart ({cart_count})
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_flash_sale_banner() -> None:
    """Render flash sale banner with countdown"""
    st.markdown(
        """
        <div style="
            background: linear-gradient(90deg, #FF9900, #2874F0);
            color: white;
            padding: 15px 20px;
            border-radius: 4px;
            text-align: center;
            font-weight: bold;
            font-size: 18px;
            margin: 10px 0;
        ">
            ⚡ Flash Sale — Limited Time Offer! Up to 50% Off on Select Items
        </div>
        """,
        unsafe_allow_html=True
    )

def render_product_card(product: Dict, col) -> None:
    """Render a single product card in a column"""
    discount = calculate_discount_percent(product)
    save_amount = calculate_save_amount(product)
    
    with col:
        st.markdown(
            f"""
            <div style="
                background: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                transition: transform 0.2s ease;
            ">
                <div style="position: relative; margin-bottom: 8px;">
                    <div style="
                        position: absolute;
                        top: 5px;
                        left: 5px;
                        background: #388e3c;
                        color: white;
                        padding: 3px 8px;
                        border-radius: 3px;
                        font-size: 11px;
                        font-weight: bold;
                    ">{discount}% OFF</div>
                    <div style="
                        position: absolute;
                        top: 5px;
                        right: 5px;
                        background: #00a650;
                        color: white;
                        padding: 3px 8px;
                        border-radius: 3px;
                        font-size: 10px;
                    ">✓ Verified Delivery</div>
                    <img src="{product['image']}" width="100%" style="border-radius: 4px;">
                </div>
                <div style="font-size: 13px; font-weight: bold; margin: 8px 0;">
                    {product['name'][:40]}...
                </div>
                <div style="font-size: 11px; color: #666; margin-bottom: 8px;">
                    {product['brand']}
                </div>
                <div style="
                    display: flex;
                    align-items: center;
                    gap: 5px;
                    font-size: 12px;
                    margin-bottom: 8px;
                ">
                    {'★' * int(product['rating'])}☆ ({product['rating']})
                    <span style="color: #666;">({product['reviews']:,} ratings)</span>
                </div>
                <div style="margin-bottom: 8px;">
                    <span style="font-size: 16px; font-weight: bold; color: #000;">
                        ₹{product['price']:,}
                    </span>
                    <span style="
                        text-decoration: line-through;
                        color: #888;
                        font-size: 12px;
                        margin-left: 5px;
                    ">₹{product['original_price']:,}</span>
                </div>
                <div style="font-size: 11px; color: #B12704; margin-bottom: 8px;">
                    {discount}% off | {save_amount}
                </div>
                {f'<div style="font-size: 11px; color: #00a650; margin-bottom: 8px;">📋 No Cost EMI from {product.get("emi", "N/A")}</div>' if product.get('emi') else '<div style="font-size: 11px; color: #666; margin-bottom: 8px;">📋 EMI not available</div>'}
                <div style="font-size: 11px; color: #666; margin-bottom: 12px;">
                    📅 Arrives in 1-3 days | 📍 Delivering to your area
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Add to Cart and Buy Now buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🛒 Add", key=f"add_{product['id']}", use_container_width=True):
                st.session_state.cart.append(product)
                st.success(f"Added {product['name'][:20]}... to cart!")
        with col2:
            if st.button("💳 Buy", key=f"buy_{product['id']}", use_container_width=True):
                st.session_state["selected_product"] = product
                st.session_state["current_page"] = "product_detail"
                st.rerun()

def render_deliverability_checker(product: Dict, location: str) -> None:
    """Render deliverability checker panel"""
    from delivery_logic import predict_deliverability, get_delivery_agencies, get_nearest_hubs, is_electronic_gadget
    
    st.markdown(
        """
        <div style="
            background: #f8f9fa;
            border: 2px solid #2874F0;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
        ">
            <div style="font-size: 16px; font-weight: bold; color: #0F1111; margin-bottom: 15px;">
                🔍 CHECK DELIVERY TO YOUR LOCATION
            </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        f"""
        <div style="background: white; padding: 10px; border-radius: 4px; margin-bottom: 10px;">
            📍 <b>Delivery Location:</b> {location}
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if st.button("🔍 Check Deliverability", key=f"check_{product['id']}", use_container_width=True):
        # Get prediction
        prediction = predict_deliverability(product, location)
        
        # Display result
        if prediction["deliverable"]:
            st.markdown(
                f"""
                <div style="
                    background: #e8f5e9;
                    border-left: 4px solid #00a650;
                    padding: 12px;
                    border-radius: 4px;
                    margin: 15px 0;
                ">
                    <div style="font-size: 14px; font-weight: bold; color: #00a650;">
                        ✅ Deliverable to {location}!
                    </div>
                    <div style="color: #666; font-size: 12px; margin-top: 5px;">
                        Confidence: <b>{prediction['confidence']}%</b> (from DNN model)
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Estimated delivery date
            st.markdown(
                f"""
                <div style="
                    background: white;
                    border: 1px solid #ddd;
                    padding: 12px;
                    border-radius: 4px;
                    margin: 10px 0;
                ">
                    <div style="font-weight: bold; margin-bottom: 8px;">📅 Estimated Delivery</div>
                    <div style="font-size: 14px; color: #2874F0;"><b>{prediction['predicted_days']} day{'s' if prediction['predicted_days'] != 1 else ''}</b></div>
                    <div style="color: #666; font-size: 12px;">Arrives by: <b>{prediction['arrival_date']}</b></div>
                    <div style="
                        background-color: {prediction['color']};
                        color: white;
                        padding: 6px 10px;
                        border-radius: 4px;
                        display: inline-block;
                        margin-top: 8px;
                        font-size: 12px;
                    ">🚚 {prediction['delivery_type']} · {prediction['predicted_days']} days</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Delivery progress
            st.markdown(
                """
                <div style="margin: 15px 0;">
                    <div style="font-weight: bold; margin-bottom: 10px;">📦 DELIVERY PROGRESS</div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <div style="text-align: center; flex: 1;">
                            <div style="
                                width: 30px;
                                height: 30px;
                                background: #FF9900;
                                border-radius: 50%;
                                margin: 0 auto;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                color: white;
                                font-size: 12px;
                            ">✓</div>
                            <div style="font-size: 11px; margin-top: 5px;">Placed</div>
                        </div>
                        <div style="flex: 1; height: 2px; background: #FF9900;"></div>
                        <div style="text-align: center; flex: 1;">
                            <div style="
                                width: 30px;
                                height: 30px;
                                background: #ddd;
                                border-radius: 50%;
                                margin: 0 auto;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                color: #666;
                                font-size: 12px;
                            ">2</div>
                            <div style="font-size: 11px; margin-top: 5px;">Packed</div>
                        </div>
                        <div style="flex: 1; height: 2px; background: #ddd;"></div>
                        <div style="text-align: center; flex: 1;">
                            <div style="
                                width: 30px;
                                height: 30px;
                                background: #ddd;
                                border-radius: 50%;
                                margin: 0 auto;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                color: #666;
                                font-size: 12px;
                            ">3</div>
                            <div style="font-size: 11px; margin-top: 5px;">Shipped</div>
                        </div>
                        <div style="flex: 1; height: 2px; background: #ddd;"></div>
                        <div style="text-align: center; flex: 1;">
                            <div style="
                                width: 30px;
                                height: 30px;
                                background: #ddd;
                                border-radius: 50%;
                                margin: 0 auto;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                color: #666;
                                font-size: 12px;
                            ">4</div>
                            <div style="font-size: 11px; margin-top: 5px;">Out</div>
                        </div>
                        <div style="flex: 1; height: 2px; background: #ddd;"></div>
                        <div style="text-align: center; flex: 1;">
                            <div style="
                                width: 30px;
                                height: 30px;
                                background: #ddd;
                                border-radius: 50%;
                                margin: 0 auto;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                color: #666;
                                font-size: 12px;
                            ">5</div>
                            <div style="font-size: 11px; margin-top: 5px;">Delivered</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Nearest delivery options (for electronic gadgets)
            if is_electronic_gadget(product.get("name", "")):
                agencies = get_delivery_agencies()
                sorted_agencies = get_nearest_hubs(location, agencies)
                
                st.markdown(
                    """
                    <div style="
                        border-top: 1px solid #ddd;
                        margin-top: 15px;
                        padding-top: 15px;
                    ">
                        <div style="font-weight: bold; margin-bottom: 12px;">
                            📦 NEAREST DELIVERY OPTIONS
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Create agency table
                agency_data = []
                for idx, agency in enumerate(sorted_agencies):
                    agency_data.append({
                        "Agency": f"{'⭐ ' if idx == 0 else ''}{agency['name']}",
                        "Hub": agency["hub"],
                        "ETA": f"{agency['eta_days']} day{'s' if agency['eta_days'] != 1 else ''}",
                        "Contact": agency["contact"]
                    })
                
                df_agencies = pd.DataFrame(agency_data)
                st.dataframe(df_agencies, use_container_width=True, hide_index=True)
                
                st.markdown(
                    """
                    <div style="font-size: 11px; color: #666; margin-top: 10px;">
                    ⭐ = Recommended (fastest to your location)
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                f"""
                <div style="
                    background: #ffebee;
                    border-left: 4px solid #cc0000;
                    padding: 12px;
                    border-radius: 4px;
                    margin: 15px 0;
                ">
                    <div style="font-size: 14px; font-weight: bold; color: #cc0000;">
                        ❌ Delivery Availability Unknown
                    </div>
                    <div style="color: #666; font-size: 12px; margin-top: 5px;">
                        We couldn't confirm delivery to <b>{location}</b>. 
                        Please contact customer support or choose a different location.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_login_card() -> None:
    """Render login form in a card"""
    st.markdown(
        """
        <div style="
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #0F1111 0%, #1a1a1a 100%);
        ">
            <div style="
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 24px rgba(0,0,0,0.15);
                padding: 40px;
                max-width: 400px;
                width: 100%;
            ">
                <div style="text-align: center; margin-bottom: 30px;">
                    <div style="font-size: 36px; margin-bottom: 10px;">🛒</div>
                    <div style="
                        font-size: 24px;
                        font-weight: bold;
                        background: linear-gradient(90deg, #FF9900, #2874F0);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        background-clip: text;
                        margin-bottom: 10px;
                    ">DeliverIQ</div>
                    <div style="font-size: 14px; color: #666;">Sign in to continue</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
