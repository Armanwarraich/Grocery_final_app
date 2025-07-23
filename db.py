import os
from pymongo import MongoClient
from datetime import datetime

# MongoDB Atlas connection (env variable preferred)
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["grocery_db"]
products_collection = db["products"]
corrections_collection = db["ocr_corrections"]
users_collection = db["users"]  # Add users collection

# Product functions
def insert_product(user_email, name, expiry, is_deleted=False):
    products_collection.insert_one({
        "user_email": user_email,
        "name": name,
        "expiry": expiry,
        "is_deleted": is_deleted
    })

def get_user_products(user_email, include_deleted=False):
    query = {"user_email": user_email}
    if not include_deleted:
        query["is_deleted"] = {"$ne": True}
    return list(products_collection.find(query))

def get_deleted_products(user_email):
    return list(products_collection.find({"user_email": user_email, "is_deleted": True}))

def add_product(user_email, name, expiry):
    products_collection.insert_one({
        "user_email": user_email,
        "name": name,
        "expiry": expiry,
        "is_deleted": False
    })

def update_product(product_id, name, expiry):
    products_collection.update_one(
        {"_id": product_id},
        {"$set": {"name": name, "expiry": expiry}}
    )

def delete_product(product_id):
    products_collection.update_one(
        {"_id": product_id},
        {"$set": {"is_deleted": True}}
    )

def restore_product(product_id):
    products_collection.update_one(
        {"_id": product_id},
        {"$set": {"is_deleted": False}}
    )

# User functions
def find_user(email):
    return users_collection.find_one({"email": email})

def create_user(email, password):
    if users_collection.find_one({"email": email}):
        return False
    users_collection.insert_one({"email": email, "password": password})
    return True

# OCR functions
def upsert_ocr_feedback(ocr_lines, user_email, pred_product, pred_expiry, final_product, final_expiry):
    """Log a correction and enable future adaptive suggestion (for your email/OCR combo)."""
    corrections_collection.replace_one(
        {
            "user_email": user_email,
            "ocr_lines": ocr_lines,
            "pred_product": pred_product,
            "pred_expiry": pred_expiry
        },
        {
            "user_email": user_email,
            "ocr_lines": ocr_lines,
            "pred_product": pred_product,
            "pred_expiry": pred_expiry,
            "final_product": final_product,
            "final_expiry": final_expiry,
            "timestamp": datetime.utcnow()
        },
        upsert=True
    )

def get_ocr_feedback(user_email, ocr_lines):
    """Return a learned correction for this OCR and user if seen before."""
    doc = corrections_collection.find_one({"user_email": user_email, "ocr_lines": ocr_lines})
    if doc:
        return doc["final_product"], doc["final_expiry"]
    return None, None
