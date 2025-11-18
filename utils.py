import time
import threading
from datetime import datetime
import logging
import os

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('load_test.log'),
        logging.StreamHandler()
    ]
)

class RateLimiter:
    """Token bucket rate limiter for controlled load testing."""
    def __init__(self, max_rate):
        self.max_rate = max_rate
        self.tokens = max_rate
        self.last_update = time.time()
        self.lock = threading.Lock()

    def acquire(self):
        with self.lock:
            now = time.time()
            elapsed = now - self.last_update
            self.tokens += elapsed * self.max_rate
            self.tokens = min(self.tokens, self.max_rate)
            self.last_update = now
            
            if self.tokens < 1:
                time.sleep(1.0 / self.max_rate)
                self.acquire()
            else:
                self.tokens -= 1

def display_menu():
    """Display the professional load testing menu."""
    print("[LOAD_TESTER] Professional Network Diagnostics v2.1")
    print("[1] UDP Protocol Stress Test")
    print("[2] TCP Connection Stress Test") 
    print("[3] HTTP Service Stress Test")
    print("[4] Exit Diagnostic Tool")

def get_valid_input(prompt, input_type=str, max_value=None):
    """Robust input validation with error handling."""
    try:
        user_input = input_type(input(prompt))
        if max_value and input_type == int:
            user_input = min(user_input, max_value)
        return user_input
    except (ValueError, TypeError):
        return None

def log_activity(message):
    """Structured logging with automatic rotation check."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    
    # Check log file size and rotate if needed
    if os.path.exists('load_test.log') and os.path.getsize('load_test.log') > 10_000_000:  # 10MB
        os.rename('load_test.log', f'load_test_{int(time.time())}.log')
    
    logging.info(message)
