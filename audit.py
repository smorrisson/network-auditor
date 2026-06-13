import nmap
from prettytable import PrettyTable
import sys

# --- Configuration ---
PORTS_TO_SCAN = "22,80,443,3389"

SERVICE_NAMES = {
    22:   "SSH",
    80:   "HTTP",
    443:  "HTTPS",
    3389: "RDP"
}

# --- Step 1: Discover live hosts on the subnet ---
def discover_hosts(subnet):
    print(f"\n[*] Scanning subnet {subnet} for live hosts...")
    nm = nmap.PortScanner()
    nm.scan(hosts=subnet, arguments="-sn")  # ping scan only

    hosts = []
    for host in nm.all_hosts():
        ip  = host
        mac = nm[host]["addresses"].get("mac", "N/A")
        try:
            hostname = nm[host].hostname()
        except Exception:
            hostname = "N/A"
        hosts.append({"ip": ip, "mac": mac, "hostname": hostname})

    return hosts

# --- Step 2: Port scan a single host ---
def scan_ports(ip):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip, ports=PORTS_TO_SCAN, arguments="-sV --open")
    results = []

    if ip not in nm.all_hosts():
        return results  # host didn't respond

    for proto in nm[ip].all_protocols():
        for port in sorted(nm[ip][proto].keys()):
            state   = nm[ip][proto][port]["state"]
            service = nm[ip][proto][port].get("name", "unknown")
            # Use our friendly name if we have one, otherwise use nmap's
            friendly = SERVICE_NAMES.get(port, service)
            results.append({
                "port":    port,
                "state":   state,
                "service": friendly
            })

    return results

# --- Step 3: Print discovery table ---
def print_host_table(hosts):
    table = PrettyTable()
    table.field_names = ["IP Address", "MAC Address", "Hostname"]
    table.align = "l"
    for h in hosts:
        table.add_row([h["ip"], h["mac"], h["hostname"]])
    print("\n=== Discovered Hosts ===")
    print(table)

# --- Step 4: Print port scan table ---
def print_port_table(host_results):
    table = PrettyTable()
    table.field_names = ["IP Address", "Port", "State", "Service"]
    table.align = "l"
    for ip, ports in host_results.items():
        if not ports:
            table.add_row([ip, "—", "no open ports found", "—"])
        else:
            for p in ports:
                table.add_row([ip, p["port"], p["state"], p["service"]])
    print("\n=== Port & Service Scan Results ===")
    print(table)

# --- Main ---
def main():
    if len(sys.argv) != 2:
        print("Usage: sudo venv/bin/python audit.py <subnet>")
        print("Example: sudo venv/bin/python audit.py 192.168.3.0/24")
        sys.exit(1)

    subnet = sys.argv[1]

    # Discover hosts
    hosts = discover_hosts(subnet)
    if not hosts:
        print("[!] No hosts found. Check your subnet or run with sudo.")
        sys.exit(0)

    print_host_table(hosts)

    # Port scan each host
    print(f"\n[*] Scanning ports {PORTS_TO_SCAN} on {len(hosts)} host(s)...")
    host_results = {}
    for h in hosts:
        ip = h["ip"]
        print(f"    Scanning {ip}...")
        host_results[ip] = scan_ports(ip)

    print_port_table(host_results)
    print("\n[*] Audit complete.\n")

if __name__ == "__main__":
    main()
