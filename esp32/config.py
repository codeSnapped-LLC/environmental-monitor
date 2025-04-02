# Sensor configuration
SENSOR_UPDATE_INTERVAL = 5  # seconds

# I2C Configuration for TinyS3
I2C_BUS = 0
SDA_PIN = 8   # Default I2C SDA on TinyS3
SCL_PIN = 9   # Default I2C SCL on TinyS3

# Board specific
LED_PIN = 18  # RGB LED data pin
BATTERY_ADC_PIN = 2  # Battery voltage sensing

# Soil sensor configuration
SOIL_DEPTH_1 = 10  # cm (configurable)
SOIL_DEPTH_2 = 30  # cm (configurable)

# Sensor calibration values
AIR_TEMP_OFFSET = 0.0
HUMIDITY_OFFSET = 0.0
SOIL_TEMP_OFFSET = 0.0
PH_OFFSET = 0.0
AIR_QUALITY_OFFSET = 0.0

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

# MQTT Authentication Options
AUTH_MODE = "CERT"  # CERT, API_KEY, or USERPASS

# Certificate Authentication
MQTT_CERT_FILE = "/certs/client.crt"
MQTT_KEY_FILE = "/certs/client.key"
MQTT_CA_FILE = "/certs/ca.crt"

# API Key Authentication
MQTT_API_KEY = None  # Set if using API keys

# Username/Password Authentication
MQTT_USER = None
MQTT_PASSWORD = None

# MQTT Configuration (for WiFi mode)
MQTT_BROKER = "your.server.ip"
MQTT_PORT = 8883  # Default TLS port
MQTT_TOPIC = "sensors/environment"
MQTT_CLIENT_ID = "esp32-tinys3"
