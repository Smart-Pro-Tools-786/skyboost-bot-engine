Import firebase_admin
from firebase_admin import credentials, db
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

# 1. Firebase Connection
# You need to download your "serviceAccountKey.json" from Firebase Settings
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://skyboost-smm-default-rtdb.firebaseio.com'
})

def start_youtube_automation(link, service_type):
    print(f"--- Starting Task for: {link} ---")
    
    # Setting up Proxies & Browser
    options = uc.ChromeOptions()
    # options.add_argument('--proxy-server=YOUR_PROXY_HERE') # Optional: Add your Proxy
    
    driver = uc.Chrome(options=options)
    
    try:
        driver.get(link)
        time.sleep(5) # Wait for page load
        
        if "Watch Hours" in service_type:
            print("Action: Increasing Watch Time...")
            # Loop to keep video running or refresh with different IPs
            time.sleep(600) # Stay on video for 10 minutes (example)
            
        elif "Subscribers" in service_type:
            print("Action: Adding Subscriber...")
            # Login logic would go here
            time.sleep(10)
            
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        driver.quit()
        print("--- Task Completed ---")

# 2. Continuous Monitoring (The "While True" Loop)
# This keeps the bot running even while you sleep
print("SkyBoost Bot is active and monitoring orders...")

while True:
    orders_ref = db.reference('active_orders')
    all_orders = orders_ref.get()

    if all_orders:
        for order_id, details in all_orders.items():
            if details['status'] == 'Processing':
                print(f"New Order Found: {order_id}")
                
                # Run the Automation
                start_youtube_automation(details['link'], details['service'])
                
                # Update status to 'Completed' in Firebase
                db.reference(f'active_orders/{order_id}').update({
                    'status': 'Completed',
                    'progress': '100%'
                })
    
    time.sleep(30) # Wait 30 seconds before checking for new orders again

