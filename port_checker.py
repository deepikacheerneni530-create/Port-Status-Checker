import socket
import ipaddress
import errno
from datetime import datetime
from pathlib import Path


def check_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((ip, port))

            if result == 0:
                return "OPEN"
            elif result == errno.ECONNREFUSED:
                return "CLOSED"
            else:
                return "FILTERED / NO RESPONSE"

    except socket.timeout:
        return "FILTERED / TIMEOUT"
    except OSError:
        return "FILTERED / ERROR"


def main():

    print("=" * 50)
    print("          PORT STATUS CHECKER")
    print("=" * 50)

    target = input("Enter target IP address: ")

    try:
        address = ipaddress.ip_address(target)

        if not (address.is_private or address.is_loopback):
            print("Only local/private IP addresses are allowed.")
            return

    except ValueError:
        print("Invalid IP address!")
        return

    try:
        start_port = int(input("Enter starting port: "))
        end_port = int(input("Enter ending port: "))

        if not (1 <= start_port <= end_port <= 65535):
            print("Invalid port range!")
            return

        if end_port - start_port + 1 > 100:
            print("Maximum 100 ports allowed.")
            return

    except ValueError:
        print("Enter valid port numbers!")
        return

    print("\nScanning started...")
    print("-" * 40)
    print("PORT       STATUS")
    print("-" * 40)

    results = []

    for port in range(start_port, end_port + 1):
        status = check_port(target, port)

        print(f"{port:<10} {status}")
        results.append(f"Port {port}: {status}")

    # Save execution log
    log_path = Path(__file__).resolve().parent / "execution_log.txt"

    with open(log_path, "a") as file:
        file.write("\n--- Port Scan Report ---\n")
        file.write(f"Date: {datetime.now()}\n")
        file.write(f"Target: {target}\n")
        file.write("\n".join(results))
        file.write("\n")

    print("-" * 40)
    print("Scanning completed!")
    print("Execution log saved at:", log_path)


if __name__ == "__main__":
    main()