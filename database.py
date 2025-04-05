import sqlite3
import datetime

def connect_db():
    """Connect to SQLite database"""
    return sqlite3.connect('bookings.db')

def initialize_db():
    """Initialize database tables"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resource TEXT,
        action TEXT,
        details TEXT,
        status TEXT,
        timestamp TEXT
    )''')
    conn.commit()
    conn.close()

def add_booking(resource, details, action, status):
    """Insert new booking record"""
    conn = connect_db()
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute('INSERT INTO bookings (resource, action, details, status, timestamp) VALUES (?, ?, ?, ?, ?)',
                   (resource, action, str(details), status, timestamp))
    conn.commit()
    conn.close()

def update_booking_status(resource, person, new_status):
    """Update booking status"""
    conn = connect_db()
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute('''
        UPDATE bookings 
        SET status = ?, timestamp = ? 
        WHERE id = (SELECT id FROM bookings 
                    WHERE resource = ? AND details LIKE ? 
                    ORDER BY id DESC LIMIT 1)
    ''', (new_status, timestamp, resource, f'%{person}%'))
    conn.commit()
    conn.close()

def list_bookings():
    """Retrieve all bookings"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings')
    bookings = cursor.fetchall()
    conn.close()
    return bookings