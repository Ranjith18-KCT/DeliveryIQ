# 🚀 DeliverIQ - Setup & Configuration Guide

## ⚡ Quick Start (2 Minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the App
```bash
streamlit run app.py
```

### Step 3: Access the App
Open your browser and go to:
```
http://localhost:8501
```

---

## 📋 Detailed Setup

### **Prerequisites**
- Python 3.10 or higher
- pip (Python package manager)
- Internet connection (for Streamlit & dependencies)

### **Installation Steps**

#### 1. Navigate to project directory
```bash
cd "c:\Ranjith\sem 4\ML project"
```

#### 2. Create a virtual environment (recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

#### 3. Install all dependencies
```bash
pip install -r requirements.txt
```

#### 4. Verify installation
```bash
python -c "import streamlit; print('✅ Streamlit installed successfully!')"
```

---

## 🏃 Running the Application

### **Standard Way**
```bash
streamlit run app.py
```

### **Using Python Script (with auto-install)**
```bash
python run_deliveriq.py
```

### **With Custom Port** (if 8501 is busy)
```bash
streamlit run app.py --server.port 8502
```

### **Headless Mode** (for servers)
```bash
streamlit run app.py --server.headless true
```

---

## 📝 Configuration Files

### **Streamlit Config** (Optional: `.streamlit/config.toml`)
Create this file in `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF9900"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#0F1111"

[client]
showErrorDetails = true
maxMessageSize = 200
toolbarMode = "viewer"

[server]
port = 8501
headless = false
runOnSave = true
```

### **Streamlit Secrets** (Optional: `.streamlit/secrets.toml`)
For sensitive data:
```toml
[api]
openai_key = "sk-..."

[database]
host = "localhost"
port = 5432
```

---

## 📁 Project File Structure

```
c:\Ranjith\sem 4\ML project\
├── app.py                          # Main Streamlit app (RUN THIS)
├── auth.py                         # Authentication & registration
├── delivery_logic.py               # Deliverability predictions
├── products.py                     # Product catalog & areas
├── ui_components.py                # Reusable UI components
├── styles.css                      # Custom CSS theme
├── users.json                      # User storage (auto-created)
├── requirements.txt                # Dependencies
├── run_deliveriq.py               # Quick start script
├── README_DELIVERIQ.md            # Full documentation
├── SETUP_GUIDE.md                 # This file
├── .streamlit/
│   └── config.toml                # Optional Streamlit config
└── backend/
    ├── app.py                      # FastAPI backend (optional)
    ├── models/
    │   ├── dnn_classifier.h5      # DNN model (optional)
    │   ├── dnn_regressor.h5       # DNN regressor (optional)
    │   └── ...
    └── routes/
```

---

## 🧪 Testing the Application

### **Test 1: Login/Register**
1. Go to "Create Account" tab
2. Enter:
   - Full Name: `Test User`
   - Email: `test@deliveriq.com`
   - Phone: `9876543210`
   - Password: `test123456`
3. Click "Create Account"
4. Sign in with same credentials

### **Test 2: Location Selection**
1. After login, select any location from dropdown
2. Click "Confirm Location"
3. Verify location shows in navbar

### **Test 3: Browse Products**
1. Use sidebar filters to narrow products
2. Search for "laptop" or "mobile"
3. See product grid update

### **Test 4: Check Deliverability**
1. Click on any product
2. Click "🔍 Check Deliverability"
3. Verify:
   - ✅ Deliverable status
   - 📅 Estimated delivery date
   - 🚚 Delivery type (Express/Standard/Economy/Delayed)
   - 📦 Agency table with nearest hub marked ⭐

### **Test 5: Shopping Cart**
1. Click "🛒 Add" on any product
2. Verify item count in navbar
3. Click "💳 Checkout"
4. See success notification

---

## 🔧 Troubleshooting

### **Issue 1: Module not found**
```
ModuleNotFoundError: No module named 'streamlit'
```
**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### **Issue 2: Port 8501 already in use**
```
Address already in use
```
**Solution:**
```bash
streamlit run app.py --server.port 8502
# or kill the process
# Windows: netstat -ano | findstr :8501
# Then: taskkill /PID <PID> /F
```

### **Issue 3: Users not persisting**
```
users.json not found / permission denied
```
**Solution:**
- Ensure `users.json` is in project root
- Check file permissions (should be writable)
- Verify JSON format: `{}`

### **Issue 4: Streamlit cache errors**
```
StreamlitAPIException or KeyError
```
**Solution:**
```bash
# Clear Streamlit cache
rm -r ~/.streamlit/
# or on Windows
rmdir %userprofile%\.streamlit /s /q
```

### **Issue 5: Python not found**
```
'python' is not recognized as an internal or external command
```
**Solution:**
- Add Python to PATH
- Or use full path: `C:\Python310\python.exe -m pip install -r requirements.txt`

---

## 📊 Monitoring & Logs

### **View Streamlit Logs**
```bash
streamlit run app.py --logger.level=debug
```

### **Suppress Warnings**
```bash
streamlit run app.py --logger.level=error
```

### **Session Info**
Go to Settings (⚙️) in Streamlit app:
- View session state
- Check browser info
- View app version

---

## 🔐 Security Checklist

- [ ] Users.json is in .gitignore
- [ ] Passwords are hashed (SHA-256)
- [ ] No credentials in code
- [ ] HTTPS enabled (if deployed)
- [ ] CORS properly configured
- [ ] Input validation on all forms
- [ ] SQL injection protection (using JSON, not DB)
- [ ] Session timeout configured

---

## 🚀 Deployment Options

### **Local Development**
```bash
streamlit run app.py --server.port 8501
```

### **Docker** (optional)
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```
```bash
docker build -t deliveriq .
docker run -p 8501:8501 deliveriq
```

### **Streamlit Cloud**
1. Push repo to GitHub
2. Go to https://share.streamlit.io
3. Connect GitHub repo
4. Deploy with one click

### **Heroku**
```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=\$PORT" > Procfile

git push heroku main
```

---

## 📈 Performance Optimization

### **Enable Caching**
```python
@st.cache_data(ttl=3600)
def load_products():
    return PRODUCTS
```

### **Reduce Reruns**
```python
# Use key parameter to avoid duplicate state
st.text_input("Name", key="name_input")
```

### **Optimize Images**
- Use compressed images
- Lazy load on scroll
- Use placeholder images during load

### **Database Query Optimization**
```python
# For future: use connection pooling
# st.connection("sql").session.execute(query)
```

---

## 🧹 Cleanup & Maintenance

### **Clear Cache**
```bash
streamlit cache clear
```

### **Clean Temporary Files**
```bash
rm -rf .streamlit/__pycache__/
rm -rf __pycache__/
```

### **Backup Users**
```bash
cp users.json users_backup_$(date +%Y%m%d).json
```

---

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Python Official Docs](https://docs.python.org/3)
- [TensorFlow Docs](https://www.tensorflow.org/docs)
- [Pandas Documentation](https://pandas.pydata.org/docs)

---

## ❓ FAQ

**Q: How do I change the port?**
A: Use `streamlit run app.py --server.port 8502`

**Q: Can I run on mobile?**
A: Use ngrok: `ngrok http 8501` and access from mobile

**Q: How to persist data longer than session?**
A: Implement database (SQLite, PostgreSQL) instead of JSON

**Q: Can I integrate payment gateway?**
A: Yes, use Razorpay/Stripe API in checkout logic

**Q: How to add more products?**
A: Add items to `PRODUCTS` list in `products.py`

**Q: How to add more delivery agencies?**
A: Add to `get_delivery_agencies()` in `delivery_logic.py`

**Q: How to add more locations?**
A: Add to `COIMBATORE_AREAS` in `products.py`

---

## 🎓 Learning Resources

### **For Beginners:**
- Start with `app.py` - understand page routing
- Then check `auth.py` - learn authentication
- Finally explore `delivery_logic.py` - understand predictions

### **For Developers:**
- Streamlit state management
- Session state across pages
- Form handling and validation
- Data filtering and display

### **For ML Developers:**
- Integration of trained models
- Prediction pipeline
- Feature preprocessing
- Model confidence scoring

---

## 📞 Support

If you encounter issues:
1. Check the **Troubleshooting** section
2. Review **FAQ** section
3. Check Streamlit logs: `--logger.level=debug`
4. Read [Streamlit Docs](https://docs.streamlit.io)

---

## ✅ Verification Checklist

Before deploying:
- [ ] All files created successfully
- [ ] Requirements installed
- [ ] App runs without errors
- [ ] Login/register works
- [ ] Product browsing works
- [ ] Deliverability checker works
- [ ] Cart functionality works
- [ ] Sign out works
- [ ] users.json created after first registration
- [ ] No security warnings

---

**Happy shopping! 🛍️🚚✨**

*For questions, refer to README_DELIVERIQ.md for detailed feature documentation.*
