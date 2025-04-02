# Sensor configuration
SENSOR_UPDATE_INTERVAL = 5  # seconds

# I2C Configuration for TinyS3
I2C_BUS = 0
SDA_PIN = 8   # Default I2C SDA on TinyS3
SCL_PIN = 9   # Default I2C SCL on TinyS3

# Board specific
LED_PIN = 18  # RGB LED data pin
BATTERY_ADC_PIN = 2  # Battery voltage sensing

# Sensor calibration values
TEMPERATURE_OFFSET = 0.0
HUMIDITY_OFFSET = 0.0

# TinyS3 specific features
HAS_PSRAM = True
HAS_BLE = True
HAS_LORA = True

# Network Configuration
NETWORK_MODE = "LORA_MESH"  # or "WIFI_DIRECT"

# WiFi Configuration
WIFI_SSID = ""
WIFI_PASSWORD = ""

# LoRa Configuration
LORA_FREQUENCY = 915000000  # Adjust based on region
LORA_NODE_ID = 1  # Unique for each node
LORA_GATEWAY_ID = 0  # 0 for gateway nodes

# MQTT Configuration (for WiFi mode)
MQTT_BROKER = "your.server.ip"
MQTT_PORT = 1883
MQTT_TOPIC = "sensors/environment"
MQTT_CLIENT_ID = "esp32-tinys3"
MQTT_USER = None
MQTT_PASSWORD = None
