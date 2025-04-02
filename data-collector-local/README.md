# Local Data Collector

A lightweight MQTT-to-SQLite data collector designed for on-premise deployment in agricultural and environmental monitoring applications.

## Features

- **Local Data Storage**: SQLite database with no external dependencies
- **MQTT Protocol**: Compatible with ESP32 sensor nodes
- **REST API**: FastAPI endpoints for data access
- **Systemd Integration**: Runs as a managed service
- **Data Retention**: Automatic pruning of old records
- **Low Resource Usage**: Optimized for Raspberry Pi and similar hardware

## Installation Options

### 1. Manual Installation (Development)

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python server.py
```

### 2. Debian Package Installation (Production)

```bash
# Build the package (requires Docker)
./build-deb.sh

# Install the package
sudo dpkg -i data-collector-local_1.0.0_all.deb

# Start the service
sudo systemctl start data-collector
```

## Configuration

Edit `/etc/default/data-collector` after installation:

```bash
# MQTT Configuration
MQTT_HOST=192.168.1.100  # Your MQTT broker IP
MQTT_PORT=1883
MQTT_TOPIC=sensors/farm1

# Optional Authentication
MQTT_USERNAME=farmuser
MQTT_PASSWORD=securepassword
```

## API Endpoints

The service provides these REST endpoints:

- `GET /health` - Service health check
- `GET /readings?limit=100` - Retrieve recent sensor readings
  - Parameters:
    - `limit`: Number of records to return (default: 100)

Example API responses:

List all devices:
```json
{
  "devices": [
    {
      "id": "esp32-field1",
      "name": "North Field Station",
      "location": "45.123,-122.456"
    },
    {
      "id": "esp32-pond1", 
      "name": "Pond Monitor",
      "location": "45.125,-122.458"
    }
  ]
}
```

Get filtered readings:
```json
{
  "readings": [
    {
      "id": 42,
      "device_id": "esp32-pond1",
      "sensor_type": "water_temp",
      "sensor_value": 18.2,
      "sensor_units": "C",
      "recorded_at": "2025-04-02T14:30:45Z"
    },
    {
      "id": 41,
      "device_id": "esp32-pond1",
      "sensor_type": "water_ph",
      "sensor_value": 7.1,
      "sensor_units": "pH",
      "recorded_at": "2025-04-02T14:25:30Z" 
    }
  ]
}
```

Example MQTT message format from devices:
```json
{
  "device_id": "esp32-field1",
  "sensors": {
    "bme280": {"measures": ["temp", "humidity"]},
    "ds18b20": {"measures": ["soil_temp"]}
  },
  "readings": {
    "air_temp": {"value": 22.5, "units": "C"},
    "humidity": {"value": 45.2, "units": "%"},
    "soil_temp_10cm": {"value": 18.3, "units": "C"}
  }
}
```

### Water Monitoring Setup
For aquatic deployments:
1. Use waterproof enclosures (IP68 rated)
2. Calibrate pH/TDS sensors monthly
3. Place sensors in flowing water when possible
4. For turbidity, avoid direct sunlight on sensor

## Database Management

The SQLite database is stored at `/opt/data-collector/sensor_data.db` by default.

### Backup Database
```bash
sudo sqlite3 /opt/data-collector/sensor_data.db ".backup /path/to/backup.db"
```

### Export Data to CSV
```bash
sqlite3 -header -csv /opt/data-collector/sensor_data.db \
  "SELECT * FROM sensor_readings;" > readings.csv
```

## Service Management

### Start/Stop Service
```bash
sudo systemctl start data-collector
sudo systemctl stop data-collector
```

### View Logs
```bash
journalctl -u data-collector -f
```

### Enable Auto-start
```bash
sudo systemctl enable data-collector
```

## Building from Source

### Prerequisites
- Docker
- Python 3.7+
- Debian packaging tools

### Build Process
```bash
# Clone repository
git clone https://github.com/codeSnapped-LLC/environmental-monitor.git
cd environmental-monitor/data-collector-local

# Build package
./build-deb.sh
```

## Troubleshooting

### Common Issues

1. **MQTT Connection Failed**
   - Verify broker is running: `mosquitto_sub -h localhost -t '#' -v`
   - Check firewall settings

2. **Database Permission Issues**
   - Ensure user has write access: 
     ```bash
     sudo chown -R data-collector:data-collector /opt/data-collector
     ```

3. **Service Not Starting**
   - Check logs: `journalctl -u data-collector -n 50`
   - Verify dependencies: `pip list`

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Style
```bash
python -m flake8 .
python -m black .
python -m isort .
```

## License

Apache 2.0 - See [LICENSE](../LICENSE) file for details.

## Support

For issues and feature requests, please open an issue on our [GitHub repository](https://github.com/codeSnapped-LLC/environmental-monitor).
