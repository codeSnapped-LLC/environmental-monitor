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
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensor_readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT,
        air_temp REAL,
        humidity REAL,
        soil_temp_10cm REAL,
        soil_temp_30cm REAL,
        ph REAL,
        air_quality INTEGER,
        water_temp REAL,
        water_ph REAL,
        water_turbidity REAL,
        water_tds REAL,
        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
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
    """Handle incoming MQTT messages"""
    try:
        data = json.loads(msg.payload.decode())
        logger.info(f"Received MQTT message: {data}")
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO sensor_readings 
        (device_id, air_temp, humidity, soil_temp_10cm, soil_temp_30cm, ph, air_quality,
         water_temp, water_ph, water_turbidity, water_tds)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("device_id", "unknown"),
            data.get("air_temp"),
            data.get("humidity"),
            data.get("soil_temp_10cm"),
            data.get("soil_temp_30cm"),
            data.get("ph"),
            data.get("air_quality"),
            data.get("water_temp"),
            data.get("water_ph"),
            data.get("water_turbidity"),
            data.get("water_tds")
        ))
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Error processing message: {e}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

@app.get("/readings")
async def get_readings(limit: int = 100):
    """Get recent sensor readings"""
    return get_recent_readings(limit)

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
