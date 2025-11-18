from datetime import datetime

def display_menu():
    """Display the main menu."""
    print("[ANONYMOUS] DDoSTool v4.0 - Professional Edition")
    print("[1] UDP Flood Attack")
    print("[2] TCP SYN Flood") 
    print("[3] HTTP Layer Raid")
    print("[4] Exit")

def get_valid_input(prompt, input_type=str, max_value=None):
    """Get and validate user input."""
    try:
        user_input = input_type(input(prompt))
        if max_value and input_type == int:
            user_input = min(user_input, max_value)
        return user_input
    except ValueError:
        return None

def log_activity(message):
    """Log thread activity with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    
    # Write to log file
    with open("attack.log", "a") as f:
        f.write(log_entry + "\n")
