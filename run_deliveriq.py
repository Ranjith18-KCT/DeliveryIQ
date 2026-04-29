#!/usr/bin/env python
"""
DeliverIQ - Quick Start Script
Run this to start the Streamlit application
"""

import subprocess
import sys
import os

def main():
    """Run the Streamlit app"""
    print("=" * 60)
    print("🛒 DeliverIQ - E-Commerce Deliverability Checker")
    print("=" * 60)
    print("\n📍 Starting application...\n")
    
    # Check if requirements are installed
    try:
        import streamlit
        import pandas
        import numpy
        print("✅ All dependencies found!\n")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📦 Installing requirements...\n")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Run Streamlit app
    print("🚀 Launching DeliverIQ on http://localhost:8501\n")
    print("=" * 60)
    
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--logger.level=error"
    ])

if __name__ == "__main__":
    main()
