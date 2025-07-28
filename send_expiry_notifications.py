import smtplib
from email.mime.text import MIMEText
from pymongo import MongoClient
from datetime import datetime, timedelta
import dateparser
import os
import dotenv   
dotenv.load_dotenv()  # Load environment variables from .env
from utils.database import users, products  # Import collections from database module

# --- CONFIG ---
MONGO_URI = os.environ.get("MONGO_URI")
if not MONGO_URI:
    raise ValueError("❌ MONGO_URI environment variable not set.")

DB_NAME = "grocery_db"
COLLECTION_NAME = "products"
USERS_COLLECTION = "users"  # Assumes you have a 'users' collection with emails

# Email config
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
TO_EMAIL = os.environ.get("TO_EMAIL")

if not all([EMAIL_ADDRESS, EMAIL_PASSWORD, TO_EMAIL]):
    raise ValueError("❌ EMAIL_ADDRESS, EMAIL_PASSWORD, or TO_EMAIL not set.")

TO_EMAILS = TO_EMAIL.split(",")

# --- FUNCTION TO SEND EMAIL ---
def send_email(subject, body, to_emails):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = ", ".join(to_emails)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_emails, msg.as_string())

        print(f"✅ Notification email sent successfully to: {', '.join(to_emails)}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

# --- MAIN ---
def main():
    try:
        print("🔍 Connecting to MongoDB...")
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)  # Added timeout for faster failure
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        users_collection = db[USERS_COLLECTION]
        
        # Test connection
        try:
            client.admin.command('ping')
            print("✅ MongoDB connection successful")
        except Exception as e:
            raise ValueError(f"❌ Failed to connect to MongoDB: {e}. Check MONGO_URI (ensure correct cluster name, username, password, and whitelist GitHub IP).")

        # Get all users
        users = list(users_collection.find({}, {"email": 1}))
        if not users:
            print("⚠️ No users found in database.")
            return

        now = datetime.now()
        target_date = now + timedelta(days=3)

        print(f"📅 Checking for products expiring on or before: {target_date.strftime('%Y-%m-%d')}")

        now = datetime.now()
        target_date = now + timedelta(days=3)

        for user in users:
            user_email = user.get("email")
            if not user_email:
                continue

            print(f"🔍 Checking products for user: {user_email}")
            
            
            products_query = {
                "user_email": user_email,
                "expiry": {
                    "$gte": now,
                    "$lte": target_date
                }
            }
        

            expiring_products = list(collection.find(products_query))

            print(f"📦 Found {len(expiring_products)} products expiring soon for {user_email}")

            if expiring_products:
                body = "🚨 GROCERY EXPIRY ALERT 🚨\n\n"
                body += f"The following {len(expiring_products)} product(s) are expiring soon:\n\n"

                for i, p in enumerate(expiring_products, 1):
                    name = p.get("name", "Unnamed Product")
                    expiry = p.get("expiry")
                    if isinstance(expiry, str):
                        expiry = dateparser.parse(expiry)
                    exp_str = expiry.strftime("%Y-%m-%d") if expiry else "Unknown"
                    body += f"{i}. 📦 {name}\n   📅 Expires: {exp_str}\n\n"

                body += "⏰ Don't forget to use or dispose of these items soon!\n\n"
                body += "---\n"
                body += "🤖 This is an automated reminder from your AI Grocery Expiry Tracker.\n"
                body += f"📧 Sent on: {now.strftime('%Y-%m-%d at %H:%M:%S')}"

                subject = f"🚨 {len(expiring_products)} Grocery Item(s) Expiring Soon!"

                if send_email(subject, body, [user_email]):
                    print(f"✅ Successfully sent expiry notification to {user_email}.")
                else:
                    print(f"❌ Failed to send notification to {user_email}")
            else:
                print(f"✅ No expiring products for {user_email}. Skipping email.")

    except Exception as e:
        print(f"❌ Error in main function: {e}")
        raise e

if __name__ == "__main__":
    print("🚀 Starting grocery expiry check...")
    main()
    print("🏁 Grocery expiry check completed!")
