import json
import sqlite3
import paho.mqtt.client as mqtt
from datetime import datetime
from config import MQTT_CONFIG, DB_FILE

def init_db():
    """Initialize SQLite database with schema"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensor_readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT,
        air_temp REAL,
        humidity REAL,
        soil_temp_10cm REAL,
        soil_temp_30cm REAL,
        ph REAL,
        air_quality INTEGER,
        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def on_message(client, userdata, msg):
    """Handle incoming MQTT messages"""
    try:
        data = json.loads(msg.payload.decode())
        print(f"Received: {data}")
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO sensor_readings 
        (device_id, air_temp, humidity, soil_temp_10cm, soil_temp_30cm, ph, air_quality)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("device_id", "unknown"),
            data.get("air_temp"),
            data.get("humidity"),
            data.get("soil_temp_10cm"),
            data.get("soil_temp_30cm"),
            data.get("ph"),
            data.get("air_quality")
        ))
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Error processing message: {e}")

def main():
    init_db()
    
    client = mqtt.Client()
    client.on_message = on_message
    
    if MQTT_CONFIG.get("username"):
        client.username_pw_set(
            MQTT_CONFIG["username"],
            MQTT_CONFIG.get("password")
        )
    
    client.connect(MQTT_CONFIG["host"], MQTT_CONFIG["port"])
    client.subscribe(MQTT_CONFIG["topic"])
    print(f"Local collector listening on {MQTT_CONFIG['topic']}...")
    
    client.loop_forever()

if __name__ == "__main__":
    main()
