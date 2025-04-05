import datetime
from database import connect_db
from openai_integration import generate_ai_warning
from config import TICKET_LIMITS

def validate_datetime(date_str, time_str=None):
    """Validate date/time format and future date"""
    try:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        if date < datetime.date.today():
            return "Date cannot be in the past"
        if time_str:
            datetime.datetime.strptime(time_str, "%H:%M")
        return None
    except ValueError as e:
        return f"Invalid format: {str(e)}. Use YYYY-MM-DD and HH:MM"

def check_ticket_limit(person, event_type, quantity=1):
    """Check ticket purchase limits"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*) FROM bookings 
        WHERE resource = ? AND details LIKE ? AND status != 'Cancelled'
    ''', (event_type, f'%{person}%'))
    current_count = cursor.fetchone()[0]
    conn.close()
    
    if current_count + quantity > TICKET_LIMITS.get(event_type, 0):
        return False, generate_ai_warning(person, event_type, current_count, quantity)
    return True, None