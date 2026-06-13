# Network Auditor

A Python-based network auditing tool built while studying for CCNA.
Each stage is a self-contained script that builds on the previous one.

---

## Scripts

| Script | Stage | Description |
|---|---|---|
| `discover.py` | Stage 1 | Subnet discovery — finds live devices via ping sweep and ARP |
| `audit.py` | Stage 2 | Port and service scanning — checks common TCP ports on each device |

---

## Stage 1 — Device Discovery (`discover.py`)

### What it does
- Performs a ping sweep across a subnet using nmap
- Identifies active devices and retrieves their MAC addresses via ARP
- Looks up the device manufacturer using the MAC address OUI prefix
- Attempts hostname resolution via nmap and reverse DNS lookup
- Displays all results in a clean, readable table

### Real-world networking concepts applied
- **CIDR notation** — used to define the scan target (e.g. 192.168.3.0/24)
- **ARP (Address Resolution Protocol)** — how MAC addresses are discovered at Layer 2
- **DHCP** — explains why a device's IP address can change between scans
- **MAC address randomization** — iPhones and modern devices rotate their MAC address for privacy, which affects OUI-based manufacturer lookups
- **Reverse DNS** — used as a fallback for hostname resolution at Layer 7
- **OUI (Organizationally Unique Identifier)** — the first 3 octets of a MAC address identify the manufacturer

### Known limitations
- **Hostnames** — most consumer devices do not broadcast hostnames on home networks, so this field often shows as unknown
- **MAC randomization** — iPhones and some Android devices use a randomized MAC address per network session, making manufacturer lookups unreliable
- **Your own device** — the scanning machine cannot ARP itself, so its MAC address shows as unavailable
- **Sleeping devices** — devices in low-power mode may not respond to pings and will not appear in results

### Usage

1. Activate the virtual environment:
```bash
cd ~/network-auditor
source venv/bin/activate
```

2. Find your subnet:
```bash
ipconfig getifaddr en0
```
Take the result (e.g. `192.168.3.86`) and replace the last octet with 0, then add `/24` — giving you `192.168.3.0/24`.

3. Run the scanner:
```bash
sudo venv/bin/python discover.py 192.168.3.0/24
```

---

## Stage 2 — Port & Service Scanning (`audit.py`)

### What it does
- Runs the same subnet discovery as Stage 1
- For each live host, scans TCP ports 22, 80, 443, and 3389
- Identifies what service is likely running on each open port
- Displays a discovery table followed by a port scan results table

### Real-world networking concepts applied
- **TCP ports** — logical endpoints that separate different types of traffic on the same device
- **Well-known ports** — port 22 (SSH), 80 (HTTP), 443 (HTTPS), 3389 (RDP) are standardised by IANA
- **Service detection** — nmap's `-sV` flag probes open ports to confirm what is actually running, not just what port number implies
- **Attack surface reduction** — every open port is a potential entry point; closing unused services is a core hardening principle
- **Management plane security** — SSH on a router is expected and correct; the risk question is whether it is exposed to the WAN or restricted to the LAN

### Known limitations
- **Firewalled devices** — many consumer devices block port scans silently, so closed ports and firewalled ports can look identical
- **Speed** — service detection (`-sV`) is significantly slower than a ping sweep; expect 1–3 minutes for a typical home network
- **Port coverage** — only four ports are scanned by default; this is intentional for learning purposes, not a full security audit

### Usage

1. Activate the virtual environment:
```bash
cd ~/network-auditor
source venv/bin/activate
```

2. Run the audit across your full subnet:
```bash
sudo venv/bin/python audit.py 192.168.3.0/24
```

3. Or scan a single device (faster for testing):
```bash
sudo venv/bin/python audit.py 192.168.3.1/32
```
The `/32` means "this one IP address only."

---

## Requirements

- macOS (tested on Apple M1)
- Python 3.x
- nmap — install via Homebrew: `brew install nmap`
- python-nmap — install in venv: `pip install python-nmap`
- prettytable — install in venv: `pip install prettytable`

---

## Roadmap

- [x] Stage 1: Device discovery — ping sweep, ARP, MAC/OUI lookup (`discover.py`)
- [x] Stage 2: Port and service scanning (`audit.py`)
- [ ] Stage 3: Topology inference
- [ ] Stage 4: Audit flags for misconfigurations
- [ ] Stage 5: Web dashboard with visual topology map

---

## Certifications

CompTIA Tech+ | CompTIA Network+ | CCNA (in progress)
