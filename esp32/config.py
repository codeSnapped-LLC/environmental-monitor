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
