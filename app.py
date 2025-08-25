from flask import Flask, render_template, jsonify, request
import sqlite3
import threading
import time
import random
from datetime import datetime
import json

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('plant_monitoring.db')
    cursor = conn.cursor()
    
    # Create hydroponics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hydroponics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ph REAL,
            temperature REAL,
            humidity REAL,
            water_level REAL,
            light_intensity REAL,
            ec REAL,
            source TEXT DEFAULT 'internal'
        )
    ''')
    
    # Create aquaponics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS aquaponics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ph REAL,
            temperature REAL,
            humidity REAL,
            water_level REAL,
            dissolved_oxygen REAL,
            ammonia REAL,
            nitrate REAL,
            source TEXT DEFAULT 'internal'
        )
    ''')
    
    # Create devices table for managing external data sources
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT UNIQUE,
            device_name TEXT,
            device_type TEXT,
            system_type TEXT,
            last_seen TEXT,
            registered_at TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# Simulate internal sensor data collection
def collect_internal_sensor_data():
    while True:
        # Simulate hydroponics data
        hydroponics_data = {
            'timestamp': datetime.now().isoformat(),
            'ph': round(random.uniform(5.5, 6.5), 2),
            'temperature': round(random.uniform(18, 25), 2),
            'humidity': round(random.uniform(40, 70), 2),
            'water_level': round(random.uniform(50, 100), 2),
            'light_intensity': round(random.uniform(5000, 10000), 2),
            'ec': round(random.uniform(1.2, 2.5), 2),  # Electrical conductivity
            'source': 'internal'
        }
        
        # Simulate aquaponics data
        aquaponics_data = {
            'timestamp': datetime.now().isoformat(),
            'ph': round(random.uniform(6.8, 7.5), 2),
            'temperature': round(random.uniform(20, 28), 2),
            'humidity': round(random.uniform(50, 80), 2),
            'water_level': round(random.uniform(60, 100), 2),
            'dissolved_oxygen': round(random.uniform(5, 8), 2),
            'ammonia': round(random.uniform(0.1, 1.5), 2),
            'nitrate': round(random.uniform(5, 50), 2),
            'source': 'internal'
        }
        
        # Store data in database
        store_data('hydroponics', hydroponics_data)
        store_data('aquaponics', aquaponics_data)
        
        time.sleep(30)  # Collect data every 30 seconds

def store_data(system_type, data):
    conn = sqlite3.connect('plant_monitoring.db')
    cursor = conn.cursor()
    
    if system_type == 'hydroponics':
        cursor.execute('''
            INSERT INTO hydroponics (timestamp, ph, temperature, humidity, water_level, light_intensity, ec, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['timestamp'], data['ph'], data['temperature'], data['humidity'], 
              data['water_level'], data['light_intensity'], data['ec'], data.get('source', 'external')))
    else:
        cursor.execute('''
            INSERT INTO aquaponics (timestamp, ph, temperature, humidity, water_level, dissolved_oxygen, ammonia, nitrate, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['timestamp'], data['ph'], data['temperature'], data['humidity'], 
              data['water_level'], data['dissolved_oxygen'], data['ammonia'], 
              data['nitrate'], data.get('source', 'external')))
    
    conn.commit()
    conn.close()

# Register a new external device
def register_device(device_id, device_name, device_type, system_type):
    conn = sqlite3.connect('plant_monitoring.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT OR REPLACE INTO devices (device_id, device_name, device_type, system_type, last_seen, registered_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (device_id, device_name, device_type, system_type, 
              datetime.now().isoformat(), datetime.now().isoformat()))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Error registering device: {e}")
        return False
    finally:
        conn.close()

# Update device last seen timestamp
def update_device_heartbeat(device_id):
    conn = sqlite3.connect('plant_monitoring.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            UPDATE devices SET last_seen = ? WHERE device_id = ?
        ''', (datetime.now().isoformat(), device_id))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating device heartbeat: {e}")
        return False
    finally:
        conn.close()

# API Routes for external data input
@app.route('/api/data/hydroponics', methods=['POST'])
def receive_hydroponics_data():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['ph', 'temperature', 'device_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Add timestamp if not provided
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now().isoformat()
        
        # Set source to device_id
        data['source'] = data['device_id']
        
        # Register/update device
        device_name = data.get('device_name', 'Unknown Hydroponics Sensor')
        device_type = data.get('device_type', 'sensor')
        register_device(data['device_id'], device_name, device_type, 'hydroponics')
        update_device_heartbeat(data['device_id'])
        
        # Store the data
        store_data('hydroponics', data)
        
        return jsonify({'message': 'Data received successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/data/aquaponics', methods=['POST'])
def receive_aquaponics_data():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['ph', 'temperature', 'device_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Add timestamp if not provided
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now().isoformat()
        
        # Set source to device_id
        data['source'] = data['device_id']
        
        # Register/update device
        device_name = data.get('device_name', 'Unknown Aquaponics Sensor')
        device_type = data.get('device_type', 'sensor')
        register_device(data['device_id'], device_name, device_type, 'aquaponics')
        update_device_heartbeat(data['device_id'])
        
        # Store the data
        store_data('aquaponics', data)
        
        return jsonify({'message': 'Data received successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/devices', methods=['GET'])
def get_devices():
    conn = sqlite3.connect('plant_monitoring.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM devices ORDER BY last_seen DESC')
    devices = cursor.fetchall()
    
    formatted_devices = []
    for device in devices:
        formatted_devices.append({
            'id': device[0],
            'device_id': device[1],
            'device_name': device[2],
            'device_type': device[3],
            'system_type': device[4],
            'last_seen': device[5],
            'registered_at': device[6]
        })
    
    conn.close()
    return jsonify(formatted_devices)

# Dashboard Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hydroponics')
def hydroponics_dashboard():
    return render_template('hydroponics.html')

@app.route('/aquaponics')
def aquaponics_dashboard():
    return render_template('aquaponics.html')

@app.route('/devices')
def devices_dashboard():
    return render_template('devices.html')

# Data API Routes
@app.route('/api/hydroponics/data')
def get_hydroponics_data():
    conn = sqlite3.connect('plant_monitoring.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM hydroponics ORDER BY id DESC LIMIT 50')
    data = cursor.fetchall()
    conn.close()
    
    # Format data for JSON response
    formatted_data = []
    for row in data:
        formatted_data.append({
            'id': row[0],
            'timestamp': row[1],
            'ph': row[2],
            'temperature': row[3],
            'humidity': row[4],
            'water_level': row[5],
            'light_intensity': row[6],
            'ec': row[7],
            'source': row[8]
        })
    
    return jsonify(formatted_data)

@app.route('/api/aquaponics/data')
def get_aquaponics_data():
    conn = sqlite3.connect('plant_monitoring.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM aquaponics ORDER BY id DESC LIMIT 50')
    data = cursor.fetchall()
    conn.close()
    
    # Format data for JSON response
    formatted_data = []
    for row in data:
        formatted_data.append({
            'id': row[0],
            'timestamp': row[1],
            'ph': row[2],
            'temperature': row[3],
            'humidity': row[4],
            'water_level': row[5],
            'dissolved_oxygen': row[6],
            'ammonia': row[7],
            'nitrate': row[8],
            'source': row[9]
        })
    
    return jsonify(formatted_data)

if __name__ == '__main__':
    init_db()
    
    # Start sensor data collection in a separate thread
    sensor_thread = threading.Thread(target=collect_internal_sensor_data)
    sensor_thread.daemon = True
    sensor_thread.start()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
