import time
from machine import Pin, I2C
from sensors import EnvironmentalSensor
from config import SENSOR_UPDATE_INTERVAL

def main():
    # Initialize sensor
    sensor = EnvironmentalSensor()
    
    print("ESP32 Environmental Sensor Starting...")
    
    while True:
        # Read sensor data
        temp = sensor.read_temperature()
        humidity = sensor.read_humidity()
        air_quality = sensor.read_air_quality()
        
        # Print readings
        print(f"Temperature: {temp:.1f}°C")
        print(f"Humidity: {humidity:.1f}%")
        print(f"Air Quality: {air_quality} ppm")
        print("---")
        
        # Wait before next reading
        time.sleep(SENSOR_UPDATE_INTERVAL)

if __name__ == "__main__":
    main()
