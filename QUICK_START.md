# ⚡ DeliverIQ - Getting Started in 60 Seconds

## 🏃 Quick Start (Copy & Paste)

### **Step 1: Navigate to Project**
```bash
cd "c:\Ranjith\sem 4\ML project"
```

### **Step 2: Install Dependencies** (30 seconds)
```bash
python -m pip install -r requirements.txt
```

### **Step 3: Run the App** (10 seconds)
```bash
python -m streamlit run app.py
```

### **Step 4: Open in Browser**
```
http://localhost:8501
```

✅ **Done! App is running!**

---

## 🎯 First Time User Guide

### **Test the App (5 minutes)**

**1. Register a New Account:**
- Click "Create Account" tab
- Fill in your details:
  - Name: `Test User`
  - Email: `test@test.com`
  - Phone: `9876543210`
  - Password: `test123456`
- Click "Create Account" → ✅ Success message

**2. Sign In:**
- Use same email & password
- Click "Sign In" → ✅ Redirected to location

**3. Select Location:**
- Pick any area from dropdown (e.g., "Gandhipuram")
- Click "Confirm Location" → ✅ Redirected to home

**4. Browse Products:**
- Scroll through product grid
- Try search: "laptop" or "mobile"
- Click product card

**5. Check Deliverability:**
- On product detail page
- Click "🔍 Check Deliverability"
- See ✅ status, 📅 date, 🚚 agency table

**6. Add to Cart & Checkout:**
- Click "🛒 Add" → Cart count increases
- Click "💳 Checkout" → Order placed!

**7. Sign Out:**
- Click "🚪 Sign Out" → Back to login

✅ **You're now an expert!**

---

## 📁 Project Structure

```
📦 ML project/
├── 🚀 app.py ← RUN THIS
├── 🔐 auth.py
├── 📦 delivery_logic.py
├── 🛍️ products.py
├── 🎨 ui_components.py
├── 🎨 styles.css
├── 👥 users.json (auto-created)
├── 📋 requirements.txt
├── 📚 README_DELIVERIQ.md (full guide)
├── ⚙️ SETUP_GUIDE.md (installation)
├── 🤖 DNN_INTEGRATION_GUIDE.md (ML models)
├── 🏗️ ARCHITECTURE.md (design)
└── 📝 PROJECT_SUMMARY.md (overview)
```

---

## ✨ Key Features at a Glance

| Feature | Location | Command |
|---------|----------|---------|
| **Register** | Login tab | Enter details + click register |
| **Login** | Login tab | Email + password + sign in |
| **Browse** | Home page | Scroll product grid or search |
| **Filter** | Left sidebar | Dept, brand, price, rating |
| **Search** | Top navbar | Type product name |
| **Check Delivery** | Product detail | Click "🔍 Check Deliverability" |
| **Add to Cart** | Product card | Click "🛒 Add" |
| **Checkout** | Cart section | Click "💳 Checkout" |
| **Sign Out** | Navbar | Click "🚪 Sign Out" |

---

## 🛠️ Troubleshooting 10 Seconds

### **Issue: Port 8501 busy**
```bash
streamlit run app.py --server.port 8502
```

### **Issue: Module not found**
```bash
pip install -r requirements.txt --upgrade
```

### **Issue: No changes after edit**
```bash
# Clear cache
streamlit cache clear
```

### **Issue: Users not saving**
- Check `users.json` exists in project root
- Verify write permissions

---

## 🎯 What You Can Do

✅ Register & login with hashed passwords
✅ Browse 10 electronics products
✅ Search & filter by category, price, brand, rating
✅ View product details & highlights
✅ Check delivery status with confidence %
✅ See nearest agencies sorted by ETA
✅ Add items to cart
✅ View 5-stage delivery progress
✅ View customer reviews
✅ Responsive on mobile, tablet, desktop

---

## 📊 Sample Test Data

### **Test Locations:**
- Gandhipuram
- Peelamedu
- RS Puram
- Singanallur
- Ukkadam

### **Test Products:**
- Apple MacBook Air (₹89,999)
- Samsung Galaxy S24 (₹109,999)
- OnePlus Nord CE 4 (₹24,999)
- HP Pavilion Gaming (₹67,999)
- boAt Rockerz 550 (₹1,299)

### **Test Agencies:**
- Blue Dart (1 day) ⭐
- Amazon Logistics (1 day)
- Delhivery (2 days)
- Xpressbees (2 days)
- DTDC (3 days)

---

## 🚀 Next Steps

### **To Integrate DNN Models:**
See: `DNN_INTEGRATION_GUIDE.md`

### **To Deploy Online:**
See: `SETUP_GUIDE.md` → "Deployment Options"

### **To Customize:**
Edit `products.py` → Add more products/areas

### **For Full Documentation:**
See: `README_DELIVERIQ.md`

---

## 📞 Quick Links

| Document | Purpose |
|----------|---------|
| [README_DELIVERIQ.md](README_DELIVERIQ.md) | Complete feature guide |
| [SETUP_GUIDE.md](SETUP_GUIDE.md) | Installation & configuration |
| [DNN_INTEGRATION_GUIDE.md](DNN_INTEGRATION_GUIDE.md) | Integrate ML models |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design & diagrams |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Deliverables overview |

---

## ✅ Verification Checklist

After running `streamlit run app.py`:

- [ ] App opens at http://localhost:8501
- [ ] Login page visible
- [ ] Can register new account
- [ ] Can login
- [ ] Can select location
- [ ] Can browse products
- [ ] Can search products
- [ ] Can click product details
- [ ] Can check deliverability
- [ ] Can see agencies table
- [ ] Can add to cart
- [ ] Can sign out
- [ ] No console errors

✅ **All checks passed? You're ready!**

---

## 🎓 Learning the Codebase

### **Understand in 15 minutes:**

1. **app.py** (3 min) - Main routing logic
2. **auth.py** (2 min) - Login/register functions
3. **delivery_logic.py** (2 min) - Prediction logic
4. **products.py** (1 min) - Product data
5. **ui_components.py** (5 min) - UI rendering
6. **users.json** (1 min) - User storage

### **Try modifying (10 minutes):**

1. Add new product to `products.py`
2. Change colors in `ui_components.py`
3. Add new location to `COIMBATORE_AREAS`
4. Adjust prediction logic in `delivery_logic.py`

✅ **You're now comfortable with the codebase!**

---

## 🐛 Common Issues & Fixes

| Problem | Solution |
|---------|----------|
| App won't start | `pip install streamlit` |
| Port in use | `--server.port 8502` |
| Module not found | `pip install -r requirements.txt` |
| Cache error | `streamlit cache clear` |
| Users not saved | Check `users.json` exists |
| Slow performance | Clear browser cache |

---

## 💡 Pro Tips

1. **Test with filter combinations** - Try dept + price + rating
2. **Test all 10 products** - Each has unique predictions
3. **Try all 26 locations** - See different agencies
4. **Check responsive design** - Resize browser window
5. **Review code comments** - Learn implementation details

---

## 🎉 You're All Set!

Your DeliverIQ app is ready to impress! 🚀

**Remember:**
- 📝 See README_DELIVERIQ.md for full features
- ⚙️ See SETUP_GUIDE.md for deployment
- 🤖 See DNN_INTEGRATION_GUIDE.md for ML integration

**Questions?** Read the documentation files first! 📚

---

**Happy shipping! 🛍️🚚✨**

*Run `streamlit run app.py` and enjoy!*
