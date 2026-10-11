# printer_module.py
import os

def print_invoice(file_path):
    """
    Takes a file path, verifies it exists, and sends it 
    to the default printer using operating system commands.
    """
    try:
        if not os.path.exists(file_path):
            print(f"Error: File not found at {file_path}")
            return False
            
        # Get absolute path for reliability
        absolute_path = os.path.abspath(file_path)
        
        # Trigger default PDF reader/handler to print
        os.startfile(absolute_path, "print")
        print(f"Print job successfully dispatched for: {absolute_path}")
        return True
        
    except Exception as err:
        print(f"Failed to send document to printer: {err}")
        return False