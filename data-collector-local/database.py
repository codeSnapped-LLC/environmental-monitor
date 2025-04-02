import sqlite3
from datetime import datetime, timedelta
from config import DB_FILE, MAX_RECORDS

def get_recent_readings(limit=100):
    """Get most recent sensor readings"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM sensor_readings 
    ORDER BY recorded_at DESC 
    LIMIT ?
    """, (limit,))
    results = cursor.fetchall()
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
