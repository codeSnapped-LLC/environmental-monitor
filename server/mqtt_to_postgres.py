import json
import time
import psycopg2
import paho.mqtt.client as mqtt
from datetime import datetime

# Authentication Configuration
AUTH_MODE = "CERT"  # CERT, API_KEY, or USERPASS

# Certificate Authentication
MQTT_CA_FILE = "certs/ca.crt"
MQTT_CERT_FILE = "certs/server.crt"
MQTT_KEY_FILE = "certs/server.key"

# API Key Authentication
MQTT_API_KEY = None  # Set if using API keys

# Username/Password Authentication
MQTT_USER = None
MQTT_PASSWORD = None

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 8883  # Default TLS port
MQTT_TOPIC = "sensors/environment"
POSTGRES_CONFIG = {
    "host": "localhost",
    "database": "sensor_data",
    "user": "postgres",
    "password": "yourpassword"
}

def create_table(conn):
    """Create sensor data table if not exists"""
    sql = """
    CREATE TABLE IF NOT EXISTS sensor_readings (
        id SERIAL PRIMARY KEY,
        device_id VARCHAR(50),
        air_temp FLOAT,
        humidity FLOAT,
        soil_temp_10cm FLOAT,
        soil_temp_30cm FLOAT,
        ph FLOAT,
        air_quality INTEGER,
        recorded_at TIMESTAMPTZ DEFAULT NOW()
    )
    """
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()

def on_message(client, userdata, msg):
    """Handle incoming MQTT messages"""
    try:
        data = json.loads(msg.payload.decode())
        print(f"Received: {data}")
        
        # Connect to PostgreSQL
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        
        # Insert data
        sql = """
        INSERT INTO sensor_readings 
        (device_id, temperature, humidity, air_quality, recorded_at)
        VALUES (%s, %s, %s, %s, %s)
        """
        with conn.cursor() as cur:
            cur.execute(sql, (
                data.get("device_id", "unknown"),
                data["temperature"],
                data["humidity"],
                data["air_quality"],
                datetime.fromtimestamp(data["timestamp"])
            ))
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Error processing message: {e}")

def main():
    # Initialize PostgreSQL
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    create_table(conn)
    conn.close()
    
    # Setup MQTT client with authentication
    client = mqtt.Client()
    client.on_message = on_message
    
    if AUTH_MODE == "CERT":
        client.tls_set(
            ca_certs=MQTT_CA_FILE,
            certfile=MQTT_CERT_FILE,
            keyfile=MQTT_KEY_FILE
        )
    elif AUTH_MODE == "API_KEY":
        client.username_pw_set(MQTT_API_KEY, "")
    else:  # USERPASS
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.subscribe(MQTT_TOPIC)
    print(f"Listening for messages on {MQTT_TOPIC}...")
    
    client.loop_forever()

if __name__ == "__main__":
    main()
