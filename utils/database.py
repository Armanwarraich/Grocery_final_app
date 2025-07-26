import pymongo
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['grocery_tracker']  # Database name

# Collections
users = db['users']
products = db['products']
deleted_products = db['deleted_products']
ocr_feedback = db['ocr_feedback']

def get_user_products(user_email):
    """Get all products for a user"""
    return list(products.find({"user_email": user_email}))

def get_deleted_products(user_email):
    """Get deleted products for a user"""
    return list(deleted_products.find({"user_email": user_email}))

def add_product(user_email, name, expiry):
    """Add a new product"""
    product = {
        "user_email": user_email,
        "name": name,
        "expiry": expiry,
        "added_at": datetime.now()
    }
    products.insert_one(product)

def update_product(product_id, new_name, new_expiry):
    """Update product details"""
    products.update_one(
        {"_id": product_id},
        {"$set": {"name": new_name, "expiry": new_expiry}}
    )

def delete_product(product_id):
    """Move product to deleted collection"""
    product = products.find_one({"_id": product_id})
    if product:
        deleted_products.insert_one(product)
        products.delete_one({"_id": product_id})

def restore_product(product_id):
    """Restore from deleted to active products"""
    product = deleted_products.find_one({"_id": product_id})
    if product:
        products.insert_one(product)
        deleted_products.delete_one({"_id": product_id})

def get_ocr_feedback(user_email, image_path):
    """Get existing OCR feedback (stub - implement as needed)"""
    feedback = ocr_feedback.find_one({"user_email": user_email, "image_path": image_path})
    if feedback:
        return feedback['user_product'], feedback['user_expiry']
    return None, None

def upsert_ocr_feedback(image_path, user_email, pred_product, pred_expiry, user_product, user_expiry):
    """Log or update OCR feedback"""
    feedback = {
        "user_email": user_email,
        "image_path": image_path,
        "predicted_product": pred_product,
        "predicted_expiry": pred_expiry,
        "user_product": user_product,
        "user_expiry": user_expiry,
        "timestamp": datetime.now()
    }
    ocr_feedback.update_one(
        {"user_email": user_email, "image_path": image_path},
        {"$set": feedback},
        upsert=True
    )
