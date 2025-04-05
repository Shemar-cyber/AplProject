from database import *
from openai_integration import *
from validation import *
from lexer_parser import parser
from ast_generator import generate_ast
import tkinter as tk  # Add this import

def process_command(raw_command, parsed_command, output_box):
    """Process the parsed command"""
    try:
        if not raw_command:
            output_box.insert(tk.END, "Error: Empty command\n")
            return
            
        # Explain what the user is trying to do
        explanation = explain_user_command(raw_command)
        output_box.insert(tk.END, f"\nExplanation: {explanation}\n")
        
        if isinstance(parsed_command, str) and parsed_command.startswith("Error"):
            output_box.insert(tk.END, parsed_command + "\n")
            return
            
        # Generate AST visualization
        ast_image = generate_ast(parsed_command)
        output_box.insert(tk.END, f"\nAST generated: {ast_image}\n")
        
        if parsed_command[0] == 'LIST':
            event_type = parsed_command[1]
            if event_type not in ['concert', 'football', 'train', 'airline']:
                output_box.insert(tk.END, f"Error: Can only list concert, football, train, or airline tickets\n")
                return
                
            output_box.insert(tk.END, get_real_time_info(event_type) + "\n")
            
        elif parsed_command[0] == 'BOOK':
            details = parsed_command[1]
            if 'person' not in details or not details['person']:
                output_box.insert(tk.END, "Error: Must specify a person for booking\n")
                return
                
            if 'date' in details:
                error = validate_datetime(details['date'], details.get('time'))
                if error:
                    output_box.insert(tk.END, error + "\n")
                    return
            
            # Check ticket limits
            event_type = details['type']
            person = details['person']
            within_limit, warning = check_ticket_limit(person, event_type)
            
            if not within_limit:
                output_box.insert(tk.END, f"WARNING: {warning}\n")
                return
                    
            add_booking(event_type, details, "BOOK", "Reserved")
            output_box.insert(tk.END, f"Added booking for {person}\n")
                
        elif parsed_command[0] in ['CONFIRM', 'PAY', 'CANCEL']:
            action = parsed_command[0]
            data = parsed_command[1]
            
            if 'person' not in data or not data['person']:
                output_box.insert(tk.END, "Error: Must specify a person\n")
                return
                
            update_booking_status(data['type'], data['person'], action.capitalize())
            output_box.insert(tk.END, f"Booking {action.lower()}ed for {data['person']}\n")
                
        elif parsed_command[0] == 'VIEW':
            output_box.insert(tk.END, "\nCurrent Bookings:\n")
            bookings = list_bookings()
            if not bookings:
                output_box.insert(tk.END, "No bookings found.\n")
            else:
                for booking in bookings:
                    output_box.insert(tk.END, f"ID: {booking[0]}, Resource: {booking[1]}, Details: {booking[3]}, Status: {booking[4]}\n")
        else:
            output_box.insert(tk.END, "Unrecognized command. Type 'help' for instructions.\n")
            
    except Exception as e:
        output_box.insert(tk.END, f"Error: {str(e)}\n")
