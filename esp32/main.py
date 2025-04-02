import time
import json
from machine import Pin, I2C

# Semantic version injected by build system
FIRMWARE_VERSION = "0.1.0-dev"
from umqtt.simple import MQTTClient
from sensors import EnvironmentalSensor
from config import (
    SENSOR_UPDATE_INTERVAL, 
    MQTT_BROKER, 
    MQTT_PORT, 
    MQTT_TOPIC, 
    MQTT_CLIENT_ID, 
    MQTT_USER, 
    MQTT_PASSWORD,
    SOIL_DEPTH_1,
    SOIL_DEPTH_2,
    AUTH_MODE,
    MQTT_CERT_FILE,
    MQTT_KEY_FILE,
    MQTT_CA_FILE,
    MQTT_API_KEY
)

def connect_mqtt():
    if AUTH_MODE == "CERT":
        with open(MQTT_CERT_FILE, 'r') as f:
            cert = f.read()
        with open(MQTT_KEY_FILE, 'r') as f:
            key = f.read()
        with open(MQTT_CA_FILE, 'r') as f:
            ca = f.read()
            
        ssl_params = {
            'cert': cert,
            'key': key,
            'ca_certs': ca,
            'server_side': False
        }
        client = MQTTClient(
            MQTT_CLIENT_ID,
            MQTT_BROKER,
            port=MQTT_PORT,
            ssl=True,
            ssl_params=ssl_params
        )
    elif AUTH_MODE == "API_KEY":
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
        client.set_auth(MQTT_API_KEY, "")
    else:  # USERPASS
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT,
                          user=MQTT_USER, password=MQTT_PASSWORD)
    
    client.connect()
    return client

def main():
    # Initialize components
    sensor = EnvironmentalSensor()
    mqtt_client = connect_mqtt()
    
    print("ESP32 Environmental Sensor Starting...")
    
    while True:
        try:
            # Read sensor data
            data = {
                "air_temp": sensor.read_air_temperature(),
                "humidity": sensor.read_humidity(),
                "soil_temp_10cm": sensor.read_soil_temperature(SOIL_DEPTH_1),
                "soil_temp_30cm": sensor.read_soil_temperature(SOIL_DEPTH_2),
                "ph": sensor.read_ph(),
                "air_quality": sensor.read_air_quality(),
                "timestamp": time.time()
            }
            
            # Publish via MQTT
            mqtt_client.publish(MQTT_TOPIC, json.dumps(data))
            print(f"Published: {data}")
            
            # Wait before next reading
            time.sleep(SENSOR_UPDATE_INTERVAL)
            
        except Exception as e:
            print(f"Error: {e}")
            # Reconnect if needed
            mqtt_client = connect_mqtt()
            time.sleep(5)

if __name__ == "__main__":
    main()
