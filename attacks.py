import socket
import random
import time
from urllib.parse import urlparse
import ipaddress

def udp_probe(target_ip, port, duration, controller):
    """UDP load test with socket reuse and proper cleanup."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2.0)
    data_payload = random._urandom(512)  # Reduced payload size
    
    start_time = time.time()
    packet_count = 0
    
    while time.time() - start_time < duration and not controller.stop_flag.is_set():
        try:
            controller.rate_limiter.acquire()
            sock.sendto(data_payload, (target_ip, port))
            packet_count += 1
            if packet_count % 100 == 0:  # Log every 100 packets
                log_activity(f"UDP probe sent {packet_count} packets")
        except socket.timeout:
            continue
        except Exception as e:
            log_activity(f"UDP error: {str(e)}")
            break
    sock.close()

def tcp_test(target_ip, port, duration, controller):
    """TCP connection test with connection pooling."""
    start_time = time.time()
    connection_count = 0
    
    while time.time() - start_time < duration and not controller.stop_flag.is_set():
        try:
            controller.rate_limiter.acquire()
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(5.0)
                sock.connect((target_ip, port))
                connection_count += 1
                if connection_count % 10 == 0:
                    log_activity(f"TCP test established {connection_count} connections")
        except Exception as e:
            log_activity(f"TCP connection failed: {str(e)}")
            time.sleep(1)  # Backoff on errors

def http_test(target_ip, port, duration, controller):
    """HTTP load test with proper session handling."""
    start_time = time.time()
    request_count = 0
    
    while time.time() - start_time < duration and not controller.stop_flag.is_set():
        try:
            controller.rate_limiter.acquire()
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(10.0)
                sock.connect((target_ip, port))
                request = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\nUser-Agent: LoadTest/1.0\r\n\r\n"
                sock.send(request.encode())
                response = sock.recv(1024)
                request_count += 1
                if request_count % 5 == 0:
                    log_activity(f"HTTP test completed {request_count} requests")
        except Exception as e:
            log_activity(f"HTTP request failed: {str(e)}")

def validate_ip(ip):
    """Strict IP validation using ipaddress module."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

attack_modes = {
    "1": {"name": "UDP_LOAD_TEST", "function": udp_probe},
    "2": {"name": "TCP_CONNECTION_TEST", "function": tcp_test},
    "3": {"name": "HTTP_LOAD_TEST", "function": http_test}
}
