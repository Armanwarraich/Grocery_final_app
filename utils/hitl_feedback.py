import datetime
from db import corrections_collection

def log_hitl_feedback(user_email, image_path, detected_product, detected_expiry, corrected_product, corrected_expiry):
    feedback_entry = {
        "user_email": user_email,
        "image_path": image_path,
        "detected_product": detected_product,
        "detected_expiry": detected_expiry,
        "corrected_product": corrected_product,
        "corrected_expiry": corrected_expiry,
        "timestamp": datetime.datetime.utcnow(),
    }
    corrections_collection.insert_one(feedback_entry)
