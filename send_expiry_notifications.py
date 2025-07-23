import smtplib
from email.mime.text import MIMEText
from pymongo import MongoClient
from datetime import datetime, timedelta
import dateparser
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# --- CONFIG ---
MONGO_URI = os.environ.get("MONGO_URI")
if not MONGO_URI:
    raise ValueError("❌ MONGO_URI environment variable not set. Please add it to your .env file or environment.")

DB_NAME = "grocery_db"
COLLECTION_NAME = "products"

# Email config
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
TO_EMAILS = os.environ.get("TO_EMAIL")

if not all([EMAIL_ADDRESS, EMAIL_PASSWORD, TO_EMAILS]):
    raise ValueError("❌ EMAIL_ADDRESS, EMAIL_PASSWORD, or TO_EMAIL not set in environment.")

TO_EMAILS = TO_EMAILS.split(",")

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
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        client.admin.command('ping')
        print("✅ MongoDB connection successful")

        now = datetime.now()
        target_date = now + timedelta(days=3)

        print(f"📅 Checking for products expiring on: {target_date.strftime('%Y-%m-%d')}")

        lower_bound = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
        upper_bound = target_date.replace(hour=23, minute=59, second=59, microsecond=999999)

        products = list(collection.find({
            "expiry": {
                "$gte": lower_bound,
                "$lte": upper_bound
            }
        }))

        print(f"📦 Found {len(products)} products expiring in 3 days")

        if not products:
            print("✅ No products expiring in 3 days. No email needed.")
            return

        body = "🚨 GROCERY EXPIRY ALERT 🚨\n\n"
        body += f"The following {len(products)} product(s) are expiring in 3 days:\n\n"

        for i, p in enumerate(products, 1):
            name = p.get("name", "Unnamed Product")
            expiry = p.get("expiry")
            if isinstance(expiry, str):
                expiry = dateparser.parse(expiry)
            exp_str = expiry.strftime("%Y-%m-%d") if expiry else "Unknown"
            body += f"{i}. 📦 {name}\n   📅 Expires: {exp_str}\n\n"

        body += "⏰ Don't forget to use or dispose of these items soon!\n\n"
        body += "---\n"
        body += "🤖 This is an automated reminder from your AI Grocery Expiry Tracker.\n"
        body += f"📧 Sent on: {now.strftime('%Y-%m-%d at %H:%M:%S')}"

        subject = f"🚨 {len(products)} Grocery Item(s) Expiring Soon!"
        if send_email(subject, body, TO_EMAILS):
            print(f"✅ Successfully sent expiry notification to {len(TO_EMAILS)} recipients.")
        else:
            print("❌ Failed to send notification email")

    except Exception as e:
        print(f"❌ Error in main function: {e}")
        raise e

if __name__ == "__main__":
    print("🚀 Starting grocery expiry check...")
    main()
    print("🏁 Grocery expiry check completed!")
