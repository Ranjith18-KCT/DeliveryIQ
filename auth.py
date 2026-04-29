"""
Authentication Module
Handles user login, registration, and session management
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, Tuple, Optional

USERS_FILE = Path(__file__).parent / "users.json"

def load_users() -> Dict:
    """Load registered users from JSON file"""
    if USERS_FILE.exists():
        try:
            with open(USERS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_users(users: Dict) -> bool:
    """Save users to JSON file"""
    try:
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=2)
        return True
    except IOError as e:
        print(f"Error saving users: {e}")
        return False

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(email: str, full_name: str, phone: str, password: str, confirm_password: str) -> Tuple[bool, str]:
    """
    Register a new user
    Returns: (success: bool, message: str)
    """
    # Validate inputs
    if not email or not full_name or not phone or not password:
        return False, "All fields are required"
    
    if password != confirm_password:
        return False, "Passwords do not match"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    
    if len(phone) != 10 or not phone.isdigit():
        return False, "Phone number must be 10 digits"
    
    # Check if user already exists
    users = load_users()
    if email in users:
        return False, "Email already registered"
    
    # Hash password and store user
    users[email] = {
        "full_name": full_name,
        "phone": phone,
        "password_hash": hash_password(password)
    }
    
    if save_users(users):
        return True, "Account created successfully! Please sign in."
    else:
        return False, "Error saving user. Please try again."

def login_user(email: str, password: str) -> Tuple[bool, str, Optional[str]]:
    """
    Authenticate user login
    Returns: (success: bool, message: str, full_name: Optional[str])
    """
    if not email or not password:
        return False, "Email and password are required", None
    
    users = load_users()
    if email not in users:
        return False, "Invalid email or password", None
    
    user = users[email]
    if user["password_hash"] != hash_password(password):
        return False, "Invalid email or password", None
    
    return True, "Login successful", user["full_name"]

def validate_email(email: str) -> bool:
    """Basic email validation"""
    return "@" in email and "." in email

def validate_phone(phone: str) -> bool:
    """Validate phone number (10 digits)"""
    return len(phone) == 10 and phone.isdigit()
