# Environmental Monitoring System

A complete IoT solution for monitoring environmental conditions using ESP32 and iOS.

## System Architecture

```mermaid
graph TD
    A[ESP32 Sensor] -->|MQTT| B[Collection Server]
    B -->|SQL| C[(PostgreSQL)]
    D[iOS App] -->|BLE/WiFi| A
    D -->|HTTP| B
```

## Components

### 1. ESP32 Sensor Node
- Measures temperature, humidity, and air quality
- Sends data via MQTT to collection server
- Supports both WiFi and BLE connectivity

### 2. Collection Server
- MQTT subscriber receiving sensor data
- Stores data in PostgreSQL database
- Provides REST API for clients

### 3. iOS Monitoring App
- Displays real-time sensor data
- Connects via BLE (direct) or WiFi (through server)
- Historical data visualization

## Hardware Setup

### ESP32 TinyS3 Connections
```mermaid
graph LR
    A[Temperature Sensor] -->|I2C| B(ESP32)
    C[Humidity Sensor] -->|I2C| B
    D[Air Quality Sensor] -->|I2C| B
    B -->|WiFi| E[Router]
    B -->|BLE| F[iOS App]
```

Pin Configuration:
- I2C SDA: GPIO8
- I2C SCL: GPIO9
- Status LED: GPIO18

## Setup Instructions

### ESP32 Requirements
```bash
micropython -m upip install umqtt.simple
```

### Server Requirements
```bash
pip install -r server/requirements.txt
```

### PostgreSQL Setup
```bash
sudo -u postgres createdb sensor_data
sudo -u postgres psql -c "CREATE USER collector WITH PASSWORD 'yourpassword';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE sensor_data TO collector;"
```

## Running the System

1. Start MQTT broker:
```bash
mosquitto -v
```

2. Start collection server:
```bash
python server/mqtt_to_postgres.py
```

3. Flash ESP32 with `main.py`

4. Build and run iOS app in Xcode

## Troubleshooting

### Common ESP32 Issues
1. **MQTT Connection Failed**
   - Verify broker IP in `config.py`
   - Check network connectivity
   - Test with `mosquitto_sub -t sensors/#`

2. **I2C Sensor Not Detected**
   - Run I2C scanner:
   ```python
   from machine import I2C, Pin
   i2c = I2C(0, sda=Pin(8), scl=Pin(9))
   print(i2c.scan())
   ```

3. **Memory Errors**
   - Enable PSRAM in firmware
   - Reduce sensor update interval

### Server Issues
1. **Database Connection Failed**
   - Verify PostgreSQL service is running
   - Check credentials in `mqtt_to_postgres.py`

2. **MQTT Message Not Received**
   - Test broker with:
   ```bash
   mosquitto_sub -t sensors/environment -v
   ```

## Future Enhancements
- [ ] Add authentication for MQTT
- [ ] Implement data encryption
- [ ] Add alerting system
- [ ] Dashboard for data visualization
- [ ] OTA firmware updates
