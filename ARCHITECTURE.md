# 📊 DeliverIQ - Architecture & Flow Diagram

## 🏗️ Application Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        STREAMLIT UI LAYER                       │
│  (Responsive frontend - Desktop, Tablet, Mobile)                │
└─────────────────────────────────────────────────────────────────┘
         │                     │                     │
         ├─────────────────────┼─────────────────────┤
         │                     │                     │
    ┌────────────┐       ┌─────────────┐     ┌───────────┐
    │  Login/    │       │  Product    │     │ Delivery  │
    │  Auth      │       │  Browsing   │     │ Checker   │
    │  Page      │       │  & Cart     │     │  Panel    │
    └────────────┘       └─────────────┘     └───────────┘
         │                     │                     │
└─────────────────────────────────────────────────────────────────┘
         │                     │                     │
         ├─────────────────────┼─────────────────────┤
         │                     │                     │
┌─────────────────────────────────────────────────────────────────┐
│                     BUSINESS LOGIC LAYER                        │
│  (Python modules handling core functionality)                   │
└─────────────────────────────────────────────────────────────────┘
         │                     │                     │
    ┌────────────┐       ┌─────────────┐     ┌───────────┐
    │  auth.py   │       │ delivery    │     │ products  │
    │  -login()  │       │ _logic.py   │     │  .py      │
    │  -register │       │ -predict()  │     │ -catalog  │
    └────────────┘       │ -agencies() │     │ -areas    │
                         └─────────────┘     └───────────┘
         │                     │                     │
└─────────────────────────────────────────────────────────────────┘
         │                     │                     │
         ├─────────────────────┼─────────────────────┤
         │                     │                     │
┌─────────────────────────────────────────────────────────────────┐
│                      DATA PERSISTENCE LAYER                     │
│  (Storage: files, optional database, ML models)                 │
└─────────────────────────────────────────────────────────────────┘
         │                     │                     │
    ┌────────────┐       ┌─────────────┐     ┌───────────┐
    │ users.json │       │   DNN       │     │ Product   │
    │ -encrypted │       │   Models    │     │  Images   │
    │ -hashed    │       │ (optional)  │     │(placehld) │
    └────────────┘       └─────────────┘     └───────────┘
```

---

## 🔄 User Flow Diagram

```
START
  │
  ├─ Is User Logged In?
  │  └─ NO  ──────────────────────┐
  │         YES                   │
  │                               ▼
  │                        ┌─────────────────┐
  │                        │  LOGIN PAGE     │
  │                        │  ┌───────────┐  │
  │                        │  │ Sign In   │  │
  │                        │  │ Register  │  │
  │                        │  └───────────┘  │
  │                        └────────┬────────┘
  │                                 │
  │ ┌──────────────────────────────┘
  │ │
  ▼ ▼
┌───────────────────────────┐
│ Is Location Set?          │
└───────────────────────────┘
  │
  ├─ NO  ──────────────────────┐
  │      YES                    │
  │                            ▼
  │                    ┌──────────────────┐
  │                    │  HOME PAGE       │
  │                    │ ┌──────────────┐ │
  │                    │ │ Browse       │ │
  │                    │ │ Products     │ │
  │                    │ │ Filter       │ │
  │                    │ │ Search       │ │
  │                    │ │ Add to Cart  │ │
  │                    │ └──────────────┘ │
  │                    └──────────────────┘
  │                             │
  │ ┌──────────────────────────┘
  │ │
  ▼ ▼
┌─────────────────────────────────┐
│  LOCATION SELECTION PAGE        │
│  ┌───────────────────────────┐  │
│  │ Coimbatore Areas (26)     │  │
│  │ OR Manual Entry           │  │
│  │ ┌───────────────────────┐ │  │
│  │ │ Confirm Location      │ │  │
│  │ └───────────────────────┘ │  │
│  └───────────────────────────┘  │
│          │                       │
└──────────┼───────────────────────┘
           │
           ▼
      USER ON HOME PAGE
           │
           ├─ Click Product Card
           │         │
           │         ▼
           │  ┌──────────────────────────┐
           │  │ PRODUCT DETAIL PAGE      │
           │  │ ┌────────────────────┐   │
           │  │ │ Product Info       │   │
           │  │ │ Highlights         │   │
           │  │ │ Reviews            │   │
           │  │ │ [CHECK DELIVERY] ◄─┼───┐
           │  │ │ Add to Cart / Buy  │   │
           │  │ │                    │   │
           │  │ └────────────────────┘   │
           │  │                          │
           │  │ ┌─────────────────────┐  │
           │  │ │ DELIVERABILITY      │  │
           │  │ │ CHECKER PANEL       │  │
           │  │ │ ✅ Status          │  │
           │  │ │ 📅 Est. Delivery   │  │
           │  │ │ 🚚 Delivery Type   │  │
           │  │ │ 📦 Agencies Table  │  │
           │  │ │ ⭐ Recommended     │  │
           │  │ └─────────────────────┘  │
           │  └──────────────────────────┘
           │
           ├─ Add to Cart
           │         │
           │         ▼
           │    ┌──────────────────┐
           │    │ Cart Count +1    │
           │    │ ✅ Toast Message │
           │    └──────────────────┘
           │
           ├─ Click Cart
           │         │
           │         ▼
           │    ┌──────────────────────┐
           │    │ VIEW CART            │
           │    │ Items Listed         │
           │    │ Total Price          │
           │    │ ┌──────────────────┐ │
           │    │ │ CHECKOUT Button  │ │
           │    │ └──────────────────┘ │
           │    └──────────────────────┘
           │
           ├─ Sign Out
           │         │
           │         ▼
           │    ┌──────────────────┐
           │    │ Clear Session    │
           │    │ → Back to Login  │
           │    └──────────────────┘
           │
           └─ Change Location
                    │
                    ▼
              Location Selection Page (again)

```

---

## 📋 Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        app.py                              │
│                   (Main orchestrator)                       │
└─────────────────────────────────────────────────────────────┘
     │              │              │              │
     │              │              │              │
     ▼              ▼              ▼              ▼
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│ auth.py │   │products │   │delivery │   │ui_comps │
│         │   │  .py    │   │_logic   │   │  .py    │
├─────────┤   ├─────────┤   ├─────────┤   ├─────────┤
│•login   │   │•PRODUCTS│   │•predict │   │•navbar  │
│•register│   │•AREAS   │   │•agencies│   │•cards   │
│•hash    │   │•get_id()│   │•hubs    │   │•checker │
│•load/   │   │•discount│   │•gadget  │   │•login   │
│ save    │   │         │   │ check   │   │•banner  │
└─────────┘   └─────────┘   └─────────┘   └─────────┘
     │              │              │              │
     ▼              ▼              ▼              ▼
┌─────────────────────────────────────────────────────────────┐
│         Session State (st.session_state)                   │
│  ┌────────────────────────────────────────────────────────┐│
│  │ logged_in | username | user_location | location_set   ││
│  │ cart | current_page | selected_product | search_query ││
│  └────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
     │              │              │
     ▼              ▼              ▼
┌─────────────┐ ┌──────────┐ ┌──────────────┐
│ users.json  │ │Style CSS │ │ Models Dir   │
│ (persist)   │ │(CSS)     │ │ (Optional)   │
└─────────────┘ └──────────┘ └──────────────┘
```

---

## 🌐 Page Navigation Map

```
                    ┌──────────────────┐
                    │   LOGIN PAGE     │
                    └────────┬─────────┘
                             │
                    (Login/Register)
                             │
                    ┌────────▼─────────┐
                    │ LOCATION SELECT  │
                    └────────┬─────────┘
                             │
                   (Confirm Location)
                             │
                    ┌────────▼─────────┐
                    │   HOME PAGE      │◄───────┐
                    │  - Product Grid  │        │
                    │  - Filters       │        │
                    │  - Search        │        │
                    │  - Cart          │        │
                    └────────┬─────────┘        │
                             │                 │
                        (Click Product)    (Back Button)
                             │                 │
                    ┌────────▼─────────┐       │
                    │ PRODUCT DETAIL   │───────┘
                    │ - Full Info      │
                    │ - Deliverability │
                    │ - Checkout       │
                    └──────────────────┘

     Navigation Elements (Sticky):
     ┌─────────────────────────────────────┐
     │ Logo │ Location │ Search │ Cart │ U │
     └─────────────────────────────────────┘
            ▲                          ▲
            │                          │
        (Clickable) ────────── Sign Out Button
        Location Changer
```

---

## 📱 Responsive Breakpoints

```
Desktop (≥1024px)          Tablet (768px-1023px)      Mobile (<768px)
┌──────────────────┐       ┌──────────────┐          ┌──────────┐
│ Logo │Loc│Search │       │Logo│Location │          │Logo      │
│      │Cart│Profile│       │Search│Cart  │          │Search    │
├──────────────────┤       ├──────────────┤          ├──────────┤
│     │            │       │              │          │          │
│Filt │ Products   │       │  Products    │          │Products  │
│ ers │ Grid (3    │       │  Grid (2     │          │Grid (1   │
│     │ columns)   │       │  columns)    │          │column)   │
│     │            │       │              │          │          │
└──────────────────┘       └──────────────┘          └──────────┘
```

---

## 🔐 Authentication Flow

```
User Input (Email, Password)
         │
         ▼
┌────────────────────┐
│ Validate Input     │
│ - Email format     │
│ - Password length  │
└────────┬───────────┘
         │
    ┌────┴────┐
    │          │
    NO        YES
    │          │
    ▼          ▼
Error    ┌─────────────────┐
toast    │ Load users.json │
         └────────┬────────┘
                  │
              ┌───┴───┐
              │       │
            YES       NO
              │       │
              ▼       ▼
         ┌──────┐  User
         │Found │  not
         └──┬───┘  found
            │
         ┌──┴──────┐
         │          │
      Match      No
      pwd?       match
         │          │
        YES        NO
         │          │
         ▼          ▼
      ┌──────┐   Error:
      │Login │   Invalid
      │OK    │   password
      └──┬───┘   toast
         │
         ▼
    Set Session:
    - logged_in = True
    - username = name
    - email = email
    
         │
         ▼
    Redirect to
    Location Selection
```

---

## 🚚 Deliverability Prediction Pipeline

```
User Clicks "Check Deliverability"
         │
         ▼
┌────────────────────────────────┐
│ predict_deliverability()       │
│ (product, location)            │
└────────────┬───────────────────┘
             │
        ┌────┴────────────────────┐
        │                         │
        ▼                         ▼
┌───────────────────┐   ┌──────────────────┐
│ is_electronic()   │   │ Valid location?  │
│ Check keywords    │   │ In Coimbatore    │
└────────┬──────────┘   │ areas?           │
         │              └────────┬─────────┘
         │                       │
         YES             ┌───────┴────┐
         │               │            │
         ▼               NO           YES
    Confidence:      │                │
    94-99%          ▼                ▼
              Return        ┌─────────────────┐
              Not           │ Calculate Days  │
              Deliverable   └────────┬────────┘
                                     │
                    ┌────────────────┼─────────────────┐
                    │                │                 │
                 (1-2)            (3-5)            (6-9)
                    │                │                 │
                    ▼                ▼                 ▼
              Express        Standard           Economy
              (Green)        (Blue)             (Orange)
              Conf: 96%      Conf: 95%         Conf: 94%
                    │                │                 │
                    └────────────────┼─────────────────┘
                                     │
                                     ▼
                    ┌──────────────────────────────┐
                    │ Calculate Arrival Date       │
                    │ today + N days               │
                    │ Format: "Wed, 4 June 2025"   │
                    └────────────┬─────────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────────┐
                    │ get_nearest_hubs()           │
                    │ Sort by zone proximity       │
                    │ Return 7 agencies sorted     │
                    └────────────┬─────────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────────┐
                    │ Return Prediction Dict:      │
                    │ {                            │
                    │   deliverable: bool,         │
                    │   confidence: float,         │
                    │   predicted_days: int,       │
                    │   delivery_type: str,        │
                    │   arrival_date: str,         │
                    │   color: str                 │
                    │ }                            │
                    └────────────┬─────────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────────┐
                    │ render_deliverability_      │
                    │ checker()                    │
                    │ - Display result            │
                    │ - Show agency table         │
                    │ - Mark recommended ⭐       │
                    └──────────────────────────────┘
```

---

## 💳 Shopping Cart Lifecycle

```
Product Grid / Detail Page
              │
              ├─ [🛒 Add] ──────────┐
              │                      │
              ▼                      ▼
    ┌─────────────────┐    ┌──────────────────────┐
    │ Add to Cart     │    │ Cart Item Appended   │
    │ st.session_     │    │ to session_state     │
    │ state["cart"]   │    │["cart"]              │
    │ .append()       │    └──────────┬───────────┘
    └─────────────────┘               │
                                      ▼
                            ┌──────────────────────┐
                            │ Update Cart Count    │
                            │ len(st.session_      │
                            │ state["cart"])       │
                            └──────────┬───────────┘
                                       │
                            ┌──────────▼───────────┐
                            │ Success Toast:       │
                            │ "✅ Added to cart!"  │
                            └──────────┬───────────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
            [View Cart]        [Continue Shopping]   [Checkout]
                    │                  │                  │
                    ▼                  ▼                  ▼
            ┌─────────────┐    ┌───────────────┐   ┌────────────┐
            │ CART PAGE   │    │ Home Page     │   │ Process    │
            │ Items: []   │    │ Back to       │   │ Order      │
            │ Total: ₹    │    │ browsing      │   │            │
            │ [Remove]    │    │ Products      │   └────┬───────┘
            │ [Checkout]  │    └───────────────┘        │
            └─────────────┘                              ▼
                                            ┌──────────────────────┐
                                            │ Order Placed!        │
                                            │ Delivering to:       │
                                            │ {user_location}      │
                                            │                      │
                                            │ Cart Cleared         │
                                            └──────────────────────┘
```

---

## 🎨 UI Component Hierarchy

```
app.py (Main)
├── show_login_page()
│   ├── Registration Form
│   │   ├── Full Name Input
│   │   ├── Email Input
│   │   ├── Phone Input
│   │   ├── Password Input
│   │   ├── Confirm Password
│   │   └── Register Button
│   └── Login Form
│       ├── Email Input
│       ├── Password Input
│       ├── Sign In Button
│       └── Forgot Password Link
│
├── show_location_selection_page()
│   ├── Welcome Message
│   ├── Location Dropdown (26 areas)
│   ├── Manual Entry Input
│   ├── Confirm Button
│   └── Sign Out Button
│
├── show_home_page()
│   ├── render_navbar()
│   │   ├── Logo
│   │   ├── Location Display
│   │   ├── Search Bar
│   │   ├── Cart Count
│   │   └── User Info + Sign Out
│   ├── render_flash_sale_banner()
│   ├── Sidebar Filters
│   │   ├── Department Select
│   │   ├── Brand Multi-select
│   │   ├── Price Range Slider
│   │   ├── Rating Slider
│   │   ├── Delivery Filter
│   │   └── Apply Filters Button
│   ├── Product Grid
│   │   └── render_product_card() x10
│   │       ├── Product Badge
│   │       ├── Verified Badge
│   │       ├── Product Image
│   │       ├── Product Name
│   │       ├── Brand
│   │       ├── Rating Display
│   │       ├── Price Display
│   │       ├── Discount Info
│   │       ├── EMI Info
│   │       ├── Shipping Info
│   │       └── [Add] [Buy] Buttons
│   └── Cart Display
│       ├── Items List
│       ├── Total Price
│       └── Checkout Button
│
└── show_product_detail_page()
    ├── render_navbar()
    ├── Breadcrumb Navigation
    ├── Product Images
    │   ├── Main Image
    │   └── Thumbnails
    ├── Product Information
    │   ├── Title
    │   ├── Brand Link
    │   ├── Rating Bar
    │   ├── Price Block
    │   ├── Discount Badge
    │   ├── EMI Info
    │   ├── Exchange Tag
    │   └── Highlights
    ├── Action Buttons
    │   ├── Add to Cart
    │   └── Buy Now
    ├── render_deliverability_checker()
    │   ├── Location Display
    │   ├── Check Button
    │   ├── Result Section
    │   │   ├── Status Badge
    │   │   ├── Confidence Score
    │   │   └── Estimated Delivery
    │   ├── Delivery Progress Bar
    │   │   ├── Stage 1: Order Placed
    │   │   ├── Stage 2: Packed
    │   │   ├── Stage 3: Shipped
    │   │   ├── Stage 4: Out for Delivery
    │   │   └── Stage 5: Delivered
    │   └── Agency Table
    │       ├── Agency Name
    │       ├── Hub Location
    │       ├── ETA
    │       ├── Contact
    │       └── Recommended Mark
    └── Customer Reviews
        ├── Average Rating
        ├── Review 1
        ├── Review 2
        └── Review 3
```

---

## 📊 Data Flow Summary

```
User Registration/Login
         │
         ▼
Hashed Password → users.json
         │
         ▼
Session State (logged_in, username)
         │
         ▼
Location Selection
         │
         ▼
Session State (user_location, location_set)
         │
         ▼
Product Browsing
    │         │
    ├─Filter  ├─Search
    │         │
    ▼         ▼
Product Grid Display
         │
         ├─ Click Product
         │     │
         │     ▼
         │  Session State (selected_product, current_page)
         │     │
         │     ▼
         │  Product Detail Page
         │     │
         │     └─ Check Deliverability
         │            │
         │            ▼
         │     DNN Prediction
         │            │
         │            ▼
         │     Nearest Hubs Sorted
         │            │
         │            ▼
         │     Display Results
         │
         └─ Add to Cart
                │
                ▼
         Session State (cart)
                │
                ├─ View Cart
                │     │
                │     ▼
                │  Checkout
                │     │
                │     └─ Order Placed
                │
                └─ Continue Shopping
```

---

This architecture ensures scalability, maintainability, and ease of integration with your existing DNN models!
