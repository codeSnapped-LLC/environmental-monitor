import sqlite3
from datetime import datetime, timedelta
from config import DB_FILE, MAX_RECORDS

def get_device_readings(device_id, hours=None):
    """Get readings for specific device with time window"""
    query = """
    SELECT sensor_type, AVG(sensor_value) as avg_value, 
           strftime('%Y-%m-%d %H:00', recorded_at) as hour
    FROM sensor_readings
    WHERE device_id = ?
    """
    params = [device_id]
    
    if hours:
        query += " AND recorded_at > datetime('now', ?)"
        params.append(f"-{hours} hours")
    
    query += " GROUP BY sensor_type, hour ORDER BY hour"
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(query, params)
    
    # Transform into time series format
    results = {}
    for row in cursor.fetchall():
        sensor, value, hour = row
        if sensor not in results:
            results[sensor] = []
        results[sensor].append({"hour": hour, "value": value})
    
    conn.close()
    return results

def prune_old_records():
    """Maintain database size by removing oldest records"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Get current count
    cursor.execute("SELECT COUNT(*) FROM sensor_readings")
    count = cursor.fetchone()[0]
    
    if count > MAX_RECORDS:
        # Delete oldest records exceeding our limit
        cursor.execute("""
        DELETE FROM sensor_readings 
        WHERE id IN (
            SELECT id FROM sensor_readings 
            ORDER BY recorded_at ASC 
            LIMIT ?
        )
        """, (count - MAX_RECORDS,))
        conn.commit()
    
    conn.close()
