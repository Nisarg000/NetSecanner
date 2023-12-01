import subprocess
import argparse
import re
import ipaddress

def ping_scan(target):
    alive_hosts = []

    def ping_host(ip):
        result = subprocess.call(["ping", "-c", "1", ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result == 0:
            alive_hosts.append(ip)

    def calculate_ip_range(cidr):
        ip_range = list(ipaddress.IPv4Network(cidr, strict=False))
        return [str(ip) for ip in ip_range]

    def print_progress(progress):
        print(f"Pinging hosts... Progress: {progress}%\r", end='')

    if re.match(r"^\d+\.\d+\.\d+\.\d+$", target):
        ping_host(target)
    elif re.match(r"^\d+\.\d+\.\d+\.\d+-\d+\.\d+\.\d+\.\d+$", target):
        start_ip, end_ip = target.split('-')
        start_ip_parts = list(map(int, start_ip.split('.')))
        end_ip_parts = list(map(int, end_ip.split('.')))

        total_ips = 1
        for i in range(4):
            total_ips *= end_ip_parts[i] - start_ip_parts[i] + 1

        current_ip_count = 0

        while start_ip_parts <= end_ip_parts:
            ip = '.'.join(map(str, start_ip_parts))
            ping_host(ip)
            current_ip_count += 1
            progress = int(current_ip_count / total_ips * 100)
            print_progress(progress)
            for i in range(3, -1, -1):
                start_ip_parts[i] += 1
                if start_ip_parts[i] > 255:
                    start_ip_parts[i] = 0
                else:
                    break
    elif '/' in target:
        ip_range = calculate_ip_range(target)
        total_ips = len(ip_range)
        current_ip_count = 0

        for ip in ip_range:
            ping_host(ip)
            current_ip_count += 1
            progress = int(current_ip_count / total_ips * 100)
            print_progress(progress)
    elif ',' in target:
        ips = target.split(',')
        total_ips = len(ips)
        current_ip_count = 0

        for ip in ips:
            ping_host(ip.strip())
            current_ip_count += 1
            progress = int(current_ip_count / total_ips * 100)
            print_progress(progress)
    else:
        print("Invalid target format. Provide an IP address, IP range, CIDR notation, or a comma-separated list of IP addresses.")

    print_progress(100)
    print("\n")  # Print a newline to clear the line

    return alive_hosts

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ping scan for IP addresses, IP ranges, CIDR notation, or IP lists.")
    parser.add_argument("target", help="Target (IP address, IP range, CIDR notation, or comma-separated list of IPs)")
    args = parser.parse_args()

    alive_hosts = ping_scan(args.target)

    if alive_hosts:
        print("Alive Hosts:")
        for host in alive_hosts:
            print(host)
    else:
        print("No alive hosts found.")
