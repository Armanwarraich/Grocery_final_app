import schedule
import time
import threading
from send_expiry_notifications import main as send_expiry_notifications

def run_scheduler():
    """Run the scheduler in a separate thread"""
    schedule.every().day.at("20:00").do(send_expiry_notifications)
    print("🗓️ Scheduler started. Will check for expiring products daily at 8 PM.")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

def start_scheduler():
    """Start scheduler in background thread"""
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    return scheduler_thread

if __name__ == "__main__":
    # Run once immediately for testing
    print("🔧 Running expiry notification manually for testing...")
    send_expiry_notifications()

    # Then start scheduler
    run_scheduler()
