import re
from db import find_user, create_user  # Import functions instead of collections

def assess_password_strength(password):
    if len(password) < 6:
        return "Weak: too short"
    if not re.search(r"[A-Z]", password):
        return "Fair: add uppercase"
    if not re.search(r"[0-9]", password):
        return "Fair: add number"
    if not re.search(r"[^A-Za-z0-9]", password):
        return "Fair: add special character"
    return "Strong ✅"

def login_user(email, password):
    user = find_user(email)
    return user and user.get("password") == password

def register_user(email, password):
    return create_user(email, password)
