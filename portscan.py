import socket
import threading
import argparse

target = ''
port_range = ''
open_ports = set()  # Use a set to store open ports

# Lock for thread synchronization
lock = threading.Lock()

def probe_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            if result == 0:
                return port
            else:
                return None
    except Exception as e:
        return None

def scan_ports(ip, ports):
    for port in ports:
        result = probe_port(ip, port)
        if result is not None:
            with lock:
                open_ports.add(result)  # Use add to store open ports
                print(f"Port {result} is open", flush=True)

def parse_target_argument(target_argument):
    try:
        # Attempt to resolve the target_argument to an IP address
        ip = socket.gethostbyname(target_argument)
        return ip
    except socket.gaierror:
        print(f"Unable to resolve the target: {target_argument}")
        return None

def parse_port_argument(port_argument):
    port_list = []
    port_ranges = port_argument.split(',')
    
    for port_range in port_ranges:
        if '-' in port_range:
            start_port, end_port = map(int, port_range.split('-'))
            port_list.extend(range(start_port, end_port + 1))
        else:
            port_list.append(int(port_range))
    
    return port_list

def main():
    global target, port_range
    parser = argparse.ArgumentParser(description="Multi-threaded port scanner.")
    parser.add_argument("target", help="Domain name or IP address to scan")
    parser.add_argument("ports", help="Port(s) to scan (comma-separated, single port, or port range)")
    args = parser.parse_args()

    target = parse_target_argument(args.target)

    if not target:
        return

    port_list = parse_port_argument(args.ports)

    # Define the number of threads
    num_threads = 4

    # Split the port list among threads
    port_list_size = len(port_list)
    port_range_size = (port_list_size // num_threads) + 1

    threads = []

    if not port_list:
        print("No ports to scan.")
        return

    for i in range(num_threads):
        start_index = i * port_range_size
        end_index = (i + 1) * port_range_size
        thread_ports = port_list[start_index:end_index]

        if thread_ports:
            thread = threading.Thread(target=scan_ports, args=(target, thread_ports))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()

    if open_ports:
        print("Open Ports are: ")
        print(sorted(open_ports))
    else:
        print("Looks like no ports are open :(")

if __name__ == "__main__":
    main()
