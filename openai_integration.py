import os
import logging
import openai
from dotenv import load_dotenv
from config import TICKET_LIMITS

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_chatgpt_response(prompt):
    """Get response from ChatGPT"""
    try:
        if not openai.api_key:
            return "Error: OpenAI API key not configured"
            
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            timeout=10
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"OpenAI API error: {str(e)}")
        return "Sorry, I couldn't process that request right now."

def explain_user_command(raw_command):
    """Generate natural language explanation of command"""
    prompt = f"""Explain this booking system command in simple terms:
    Command: "{raw_command}"
    Respond with just 1 sentence explaining what the user wants to do. nothing more"""
    return get_chatgpt_response(prompt)

def get_real_time_info(event_type):
    """Get real-time event information"""
    prompt = f"""Generate 5 realistic example of upcoming {event_type} events in Jamaica after April 2025 with these details:
    - Event name
    - Date and time
    - Location in Jamaica
    - Available tickets
    - Price range
    Format as: "1. [Name] - [Date] at [Time] in [Location] ([Ticket info], [Price range])" """
    try:
        return get_chatgpt_response(prompt) or "Could not retrieve event information"
    except Exception as e:
        logging.error(f"Error getting real-time info: {str(e)}")
        return f"Error retrieving {event_type} events"

def generate_ai_warning(person, event_type, current_count, requested_count):
    """Generate ticket limit warning"""
    prompt = f"""Customer {person} has {current_count} {event_type} tickets and wants {requested_count} more (limit {TICKET_LIMITS[event_type]}). 
    Create polite warning explaining the limit in 2 sentences max."""
    return get_chatgpt_response(prompt)