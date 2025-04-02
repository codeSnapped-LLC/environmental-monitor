import json
import sqlite3
import paho.mqtt.client as mqtt
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import MQTT_CONFIG, DB_FILE
from database import get_recent_readings
import logging
import asyncio

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def init_db():
    """Initialize SQLite database with schema"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create device registry table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS devices (
        device_id TEXT PRIMARY KEY,
        device_name TEXT,
        location TEXT,
        last_seen TIMESTAMP,
        sensor_config TEXT
    )""")
    
    # Create sensor readings table with flexible schema
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensor_readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT,
        sensor_type TEXT,
        sensor_value REAL,
        sensor_units TEXT,
        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(device_id) REFERENCES devices(device_id)
    )""")
    
    # Create index for faster queries
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_device_sensor 
    ON sensor_readings(device_id, sensor_type)
    """)
    conn.commit()
    conn.close()

@app.on_event("startup")
async def startup_event():
    """Initialize MQTT client on startup"""
    client = mqtt.Client()
    client.on_message = on_message
    
    if MQTT_CONFIG.get("username"):
        client.username_pw_set(
            MQTT_CONFIG["username"],
            MQTT_CONFIG.get("password")
        )
    
    client.connect(MQTT_CONFIG["host"], MQTT_CONFIG["port"])
    client.subscribe(MQTT_CONFIG["topic"])
    client.loop_start()
    logger.info(f"MQTT client connected and listening on {MQTT_CONFIG['topic']}")
    app.state.mqtt_client = client

def on_message(client, userdata, msg):
    """Handle incoming MQTT messages from multiple devices"""
    try:
        data = json.loads(msg.payload.decode())
        device_id = data.get("device_id", "unknown")
        logger.info(f"Received data from device {device_id}")
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Register/update device info
        cursor.execute("""
        INSERT OR REPLACE INTO devices 
        (device_id, last_seen, sensor_config) 
        VALUES (?, CURRENT_TIMESTAMP, ?)
        """, (device_id, json.dumps(data.get("sensors", {}))))
        
        # Insert all sensor readings
        for sensor_type, reading in data.get("readings", {}).items():
            cursor.execute("""
            INSERT INTO sensor_readings 
            (device_id, sensor_type, sensor_value, sensor_units)
            VALUES (?, ?, ?, ?)
            """, (
                device_id,
                sensor_type,
                reading.get("value"),
                reading.get("units", "")
            ))
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Error processing message: {e}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

@app.get("/devices")
async def list_devices():
    """List all registered devices"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT device_id, device_name, location FROM devices")
    devices = [dict(zip(['id','name','location'], row)) for row in cursor.fetchall()]
    conn.close()
    return {"devices": devices}

@app.get("/readings")
async def get_readings(
    device_id: str = None,
    sensor_type: str = None,
    limit: int = 100,
    hours: int = None
):
    """Get sensor readings with filtering options"""
    query = "SELECT * FROM sensor_readings WHERE 1=1"
    params = []
    
    if device_id:
        query += " AND device_id = ?"
        params.append(device_id)
    if sensor_type:
        query += " AND sensor_type = ?"
        params.append(sensor_type)
    if hours:
        query += " AND recorded_at > datetime('now', ?)"
        params.append(f"-{hours} hours")
        
    query += " ORDER BY recorded_at DESC LIMIT ?"
    params.append(limit)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(query, params)
    
    columns = [col[0] for col in cursor.description]
    readings = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    
    return {"readings": readings}

if __name__ == "__main__":
    import uvicorn
    init_db()
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=False
    )
