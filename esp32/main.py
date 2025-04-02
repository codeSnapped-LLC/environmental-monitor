import time
import json
from machine import Pin, I2C
from umqtt.simple import MQTTClient
from sensors import EnvironmentalSensor
from config import SENSOR_UPDATE_INTERVAL, MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, MQTT_CLIENT_ID, MQTT_USER, MQTT_PASSWORD

def connect_mqtt():
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
                "soil_temp_10cm": sensor.read_soil_temperature(SOIL_DEPTH_1),
                "soil_temp_30cm": sensor.read_soil_temperature(SOIL_DEPTH_2),
                "ph": sensor.read_ph(),
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
