import json
import sys
import re
import hashlib

# Predefined subnets
IPV4_SUBNET = "192.168.1."
IPV6_SUBNET = "2001:db8::"

# Lease database (to prevent duplicate IP allocation)
lease_db = {}

# Function to validate MAC address
def is_valid_mac(mac):
    return re.match(r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", mac) is not None

# Function to generate IPv6 using EUI-64
def generate_ipv6(mac):
    mac = mac.replace(":", "").replace("-", "")
    mac = mac[:6] + "fffe" + mac[6:]
    ipv6 = IPV6_SUBNET + mac[:4] + ":" + mac[4:8] + ":" + mac[8:12] + mac[12:]
    return ipv6

# Function to generate IPv4 dynamically
def generate_ipv4():
    for i in range(10, 255):  # Avoiding .1-.9 for static use
        ip = f"{IPV4_SUBNET}{i}"
        if ip not in lease_db.values():
            return ip
    return None  # No available IP

# Assign IP based on DHCP type
def assign_ip(mac, dhcp_version):
    if not is_valid_mac(mac):
        return {"error": "Invalid MAC address format"}

    if mac in lease_db:
        assigned_ip = lease_db[mac]
    else:
        if dhcp_version == "DHCPv6":
            assigned_ip = generate_ipv6(mac)
        elif dhcp_version == "DHCPv4":
            assigned_ip = generate_ipv4()
            if assigned_ip is None:
                return {"error": "No available IPv4 addresses"}
        else:
            return {"error": "Invalid DHCP version"}

        lease_db[mac] = assigned_ip  # Store lease

    return {
        "mac_address": mac,
        "assigned_ip": assigned_ip,
        "lease_time": "3600 seconds"
    }

# Read input from command-line arguments
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(json.dumps({"error": "Invalid input"}))
        sys.exit(1)

    mac_address = sys.argv[1]
    dhcp_version = sys.argv[2]

    result = assign_ip(mac_address, dhcp_version)
    print(json.dumps(result))
