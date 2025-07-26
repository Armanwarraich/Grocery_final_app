import hashlib
from utils.database import users  # Now imports the 'users' collection properly

def hash_password(password):
    """Hash password for secure storage"""
    return hashlib.sha256(password.encode()).hexdigest()

def assess_password_strength(password):
    """Assess password strength (basic check)"""
    if len(password) < 8:
        return "Weak: Too short"
    if not any(c.isdigit() for c in password) or not any(c.isupper() for c in password):
        return "Medium: Add numbers and uppercase letters"
    return "Strong"

def register_user(email, password):
    """Register (sign up) a new user"""
    if users.find_one({"email": email}):
        return False  # User already exists
    
    hashed_pw = hash_password(password)
    users.insert_one({
        "email": email,
        "password": hashed_pw
    })
    return True

def login_user(email, password):
    """Log in user"""
    user = users.find_one({"email": email})
    if user and user["password"] == hash_password(password):
        return True
    return False

def add_user_to_db(email):
    from utils.database import users  # Avoids circular import
    try:
        if users.find_one({"email": email}) is None:
            users.insert_one({"email": email})
    except Exception as e:
        print(f"User insertion skipped or failed: {e}")
