import streamlit as st
from datetime import datetime ,  timedelta
import random

def get_expiry_status(expiry):
    """Determine status based on expiry date"""
    days_left = (expiry - datetime.now()).days
    if days_left < 0:
        return "Expired"
    elif days_left <= 3:
        return "Expiring Soon"
    else:
        return "Fresh"

def get_status_counts(products):
    """Count products by status"""
    expired = sum(1 for p in products if get_expiry_status(p["expiry"]) == "Expired")
    soon = sum(1 for p in products if get_expiry_status(p["expiry"]) == "Expiring Soon")
    fresh = len(products) - expired - soon
    return expired, soon, fresh

def filter_products(products, filter_option, search_term=""):
    """Filter products by option and search term"""
    filtered = products
    if search_term:
        filtered = [p for p in filtered if search_term in p["name"].lower()]
    
    if filter_option == "Expiring This Week":
        filtered = [p for p in filtered if 0 <= (datetime.now() - p["expiry"]).days <= 7]
    elif filter_option == "Expired Only":
        filtered = [p for p in filtered if p["expiry"] < datetime.now()]
    
    return filtered

def apply_theme(theme):
    """Apply theme - this is now handled in config/theme.py"""
    from config.theme import apply_theme as theme_apply
    theme_apply(theme)

def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d") if date_str else datetime.now() + timedelta(days=30)
