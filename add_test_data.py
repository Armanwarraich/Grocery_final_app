from pymongo import MongoClient
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['grocery_db']

# Add test user
users_col = db['users']
users_col.insert_one({"email": "armanwarraich4496@gmail.com"})

# Add test product expiring tomorrow
products_col = db['products']
tomorrow = datetime.now() + timedelta(days=1)
products_col.insert_one({
    "user_email": "armanwarraich4496@gmail.com",
    "name": "Test Milk",
    "expiry": tomorrow
})

print("✅ Test data added!")
