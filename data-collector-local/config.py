import os

# Database configuration
DB_FILE = "sensor_data.db"

# MQTT configuration
MQTT_CONFIG = {
    "host": "localhost",
    "port": 1883,  # Default non-TLS port for local network
    "topic": "sensors/environment",
    "username": None,  # Optional
    "password": None   # Optional
}

# Data retention settings
MAX_RECORDS = 100000  # Keep last 100k records
