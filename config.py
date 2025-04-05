# Configuration and constants
TICKET_LIMITS = {
    'concert': 4, 
    'football': 6,
    'train': 10, 
    'airline': 4
}

def show_help():
    return """SUPPORTED COMMANDS:
    - List [concert|football|train|airline] tickets in my area
    - Book train|airline from [location] to [location] on [date] at [time] for [name]
    - Book [event name] concert|football match for [name]
    - Confirm|Pay|Cancel [event type] for [name]
    - View bookings

GENERAL NOTES:
    - Dates must be in YYYY-MM-DD format (e.g., 2025-04-15)
    - Times must be in HH:MM 24-hour format (e.g., 14:30)
    - Names can be in quotes for multi-word names (e.g., "John Smith")
    - TICKET LIMITS
    Max 4 concert tickets per person
    Max 6 football tickets per person
    Max 10 train tickets per person
    Max 4 airline tickets per person"""

# Logging configuration
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)