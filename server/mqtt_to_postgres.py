import json
import time
import psycopg2
import paho.mqtt.client as mqtt
from datetime import datetime

# Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
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
        soil_temp_10cm FLOAT,
        soil_temp_30cm FLOAT,
        ph FLOAT,
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
    
    # Setup MQTT client
    client = mqtt.Client()
    client.on_message = on_message
    
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.subscribe(MQTT_TOPIC)
    print(f"Listening for messages on {MQTT_TOPIC}...")
    
    client.loop_forever()

if __name__ == "__main__":
    main()
