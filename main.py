import threading
import time
import os
import signal
import sys
from attacks import attack_modes, validate_ip
from utils import display_menu, get_valid_input, log_activity, RateLimiter

class AttackController:
    def __init__(self):
        self.stop_flag = threading.Event()
        self.active_threads = []
        self.max_threads = 500
        self.rate_limiter = RateLimiter(1000)  # 1000 requests/sec max
        
    def shutdown(self):
        """Graceful shutdown with thread joining."""
        self.stop_flag.set()
        for thread in self.active_threads:
            thread.join(timeout=2.0)
        self.active_threads.clear()
        log_activity("All threads stopped gracefully")

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully."""
    controller.shutdown()
    sys.exit(0)

def thread_worker(thread_id, target, mode_name, controller):
    """Worker thread with rate limiting and proper error handling."""
    while not controller.stop_flag.is_set():
        try:
            controller.rate_limiter.acquire()
            log_activity(f"Thread {thread_id} active | {mode_name} | {target}")
            time.sleep(2)
        except Exception as e:
            log_activity(f"Thread {thread_id} error: {str(e)}")
            break

def main():
    """Main program with proper resource management."""
    global controller
    controller = AttackController()
    signal.signal(signal.SIGINT, signal_handler)
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        display_menu()
        
        choice = input("\nEnter choice (1-4): ")
        
        if choice == "4":
            controller.shutdown()
            break
            
        if choice not in attack_modes:
            print("Invalid choice!")
            time.sleep(1)
            continue
            
        target_ip = input("Enter target IP: ")
        if not validate_ip(target_ip):
            print("Invalid IP format!")
            time.sleep(1)
            continue
            
        target_port = get_valid_input("Enter target port: ", int, 65535) or 80
        duration = get_valid_input("Duration (seconds, max 300): ", int, 300) or 60
        thread_count = min(get_valid_input("Thread count (max 250): ", int, 250) or 50, 250)

        # Start combined worker/attack threads
        for i in range(thread_count):
            t = threading.Thread(
                target=attack_modes[choice]['function'],
                args=(target_ip, target_port, duration, controller)
            )
            t.daemon = False
            t.start()
            controller.active_threads.append(t)
            time.sleep(0.05)  # Stagger thread creation

        print(f"\nLoad test started: {thread_count} threads for {duration}s")
        
        # Wait for duration or stop flag
        start_time = time.time()
        while time.time() - start_time < duration and not controller.stop_flag.is_set():
            time.sleep(1)
            active_count = sum(1 for t in controller.active_threads if t.is_alive())
            print(f"\rActive threads: {active_count}/{thread_count}", end="")
            
        controller.shutdown()
        print(f"\nLoad test completed. Press Enter to continue...")
        input()

if __name__ == "__main__":
    main()
