#!/usr/bin/env python3
"""
Stage 1 — Network Device Discovery
Scans your local subnet and prints a table of
all active devices with their IP, MAC, and hostname.
"""

import nmap
import socket
from prettytable import PrettyTable
import sys


def get_hostname(ip):
    """Try to resolve an IP to a hostname. Return the IP if it can't be resolved."""
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "(unknown)"


def discover_devices(subnet):
    """
    Run an nmap ping scan on the subnet.
    -sn means 'ping scan only' — no port scanning yet (that's Stage 2).
    --privileged tells nmap to use ARP for more accurate MAC detection.
    """
    print(f"\n🔍 Scanning {subnet} — this may take 15–30 seconds...\n")

    scanner = nmap.PortScanner()
    scanner.scan(hosts=subnet, arguments="-sn --privileged")

    devices = []

    for ip in scanner.all_hosts():
        host = scanner[ip]

        # Only include hosts that responded (are "up")
        if host.state() != "up":
            continue

        # Try to get the MAC address (may not be available for all devices)
        mac = "(not available)"
        if "mac" in host["addresses"]:
            mac = host["addresses"]["mac"]

        hostname = get_hostname(ip)

        devices.append({
            "ip": ip,
            "mac": mac,
            "hostname": hostname,
        })

    return devices


def print_table(devices):
    """Print a formatted table of discovered devices."""
    if not devices:
        print("No devices found. Try running with sudo (see instructions).")
        return

    table = PrettyTable()
    table.field_names = ["IP Address", "MAC Address", "Hostname"]
    table.align = "l"

    # Sort by the last octet of the IP so the table reads in order
    for device in sorted(devices, key=lambda d: int(d["ip"].split(".")[-1])):
        table.add_row([device["ip"], device["mac"], device["hostname"]])

    print(table)
    print(f"\n✅ Found {len(devices)} active device(s).\n")


if __name__ == "__main__":
    # Accept subnet as a command-line argument, or fall back to a default
    if len(sys.argv) > 1:
        subnet = sys.argv[1]
    else:
        subnet = "192.168.0.102/24"  # <-- change this to match your network

    devices = discover_devices(subnet)
    print_table(devices)
