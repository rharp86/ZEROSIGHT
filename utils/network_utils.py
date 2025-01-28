import socket
import concurrent.futures
from typing import List

def check_port(host: str, port: int) -> bool:
    """Check if a port is open on a given host."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        try:
            s.connect((host, port))
            return True
        except (socket.timeout, ConnectionRefusedError):
            return False

def scan_ports(host: str, ports: List[int], max_workers: int = 10) -> List[int]:
    """Scan multiple ports on a given host."""
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_port = {executor.submit(check_port, host, port): port for port in ports}
        for future in concurrent.futures.as_completed(future_to_port):
            port = future_to_port[future]
            try:
                if future.result():
                    open_ports.append(port)
            except Exception as e:
                print(f"Error checking port {port}: {e}")
    return open_ports

# Example usage
if __name__ == "__main__":
    host = "127.0.0.1"
    ports = [22, 80, 443, 8080]
    open_ports = scan_ports(host, ports)
    print(f"Open ports on {host}: {open_ports}")