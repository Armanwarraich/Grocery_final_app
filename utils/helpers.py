import streamlit as st
from datetime import datetime
import random

def get_expiry_status(expiry_date):
    if isinstance(expiry_date, str):
        import dateparser
        expiry_date = dateparser.parse(expiry_date)
    
    if not expiry_date:
        return "Unknown"
    
    days_left = (expiry_date - datetime.now()).days
    
    if days_left < 0:
        return "Expired"
    elif days_left <= 3:
        return "Expiring Soon"
    else:
        return "Fresh"

def get_status_counts(products):
    expired = sum(get_expiry_status(p["expiry"]) == "Expired" for p in products)
    soon = sum(get_expiry_status(p["expiry"]) == "Expiring Soon" for p in products)
    fresh = sum(get_expiry_status(p["expiry"]) == "Fresh" for p in products)
    return expired, soon, fresh

def filter_products(products, filter_option, search_term=""):
    now = datetime.now()
    filtered = []
    
    for p in products:
        days_left = (p["expiry"] - now).days
        
        # Apply filter
        if filter_option == "Expiring This Week" and not (0 <= days_left <= 7):
            continue
        elif filter_option == "Expired Only" and days_left >= 0:
            continue
        
        # Apply search
        if search_term and search_term not in p["name"].lower():
            continue
        
        filtered.append(p)
    
    return filtered

def apply_theme(theme):
    # Your existing theme CSS code here
    pass
