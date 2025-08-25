import requests
import time
import random
from datetime import datetime

# Server configuration
SERVER_URL = "http://localhost:5000"  # Change to your server's IP address

# Device configuration
DEVICE_ID = "hydroponics-sensor-001"
DEVICE_NAME = "Main Hydroponics Sensor"
SYSTEM_TYPE = "hydroponics"  # or "aquaponics"

def send_sensor_data():
    # Simulate sensor readings
    data = {
        "device_id": DEVICE_ID,
        "device_name": DEVICE_NAME,
        "ph": round(random.uniform(5.5, 6.5), 2),
        "temperature": round(random.uniform(18, 25), 2),
        "humidity": round(random.uniform(40, 70), 2),
        "water_level": round(random.uniform(50, 100), 2),
        "light_intensity": round(random.uniform(5000, 10000), 2),
        "ec": round(random.uniform(1.2, 2.5), 2),
        "timestamp": datetime.now().isoformat()
    }
    
    # Send data to server
    try:
        if SYSTEM_TYPE == "hydroponics":
            response = requests.post(f"{SERVER_URL}/api/data/hydroponics", json=data)
        else:
            response = requests.post(f"{SERVER_URL}/api/data/aquaponics", json=data)
        
        if response.status_code == 200:
            print(f"Data sent successfully: {data}")
        else:
            print(f"Error sending data: {response.text}")
    except Exception as e:
        print(f"Connection error: {e}")

# Send data every 30 seconds
while True:
    send_sensor_data()
    time.sleep(30)
