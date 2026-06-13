# Network Auditor

A Python-based network scanning tool built while studying for CCNA.
Discovers active devices on a local subnet and displays their IP address,
MAC address, manufacturer, and hostname in a formatted table.

---

## What it does

- Performs a ping sweep across a subnet using nmap
- Identifies active devices and retrieves their MAC addresses via ARP
- Looks up the device manufacturer using the MAC address OUI prefix
- Attempts hostname resolution via nmap and reverse DNS lookup
- Displays all results in a clean, readable table

---

## Real-world networking concepts applied

- **CIDR notation** — used to define the scan target (e.g. 192.168.3.0/24)
- **ARP (Address Resolution Protocol)** — how MAC addresses are discovered at Layer 2
- **DHCP** — explains why a device's IP address can change between scans
- **MAC address randomization** — iPhones and modern devices rotate their MAC
  address for privacy, which affects OUI-based manufacturer lookups
- **Reverse DNS** — used as a fallback for hostname resolution at Layer 7
- **OUI (Organizationally Unique Identifier)** — the first 3 octets of a MAC
  address identify the manufacturer

---

## Known limitations

- **Hostnames** — most consumer devices do not broadcast hostnames on home
  networks, so this field often shows (unknown)
- **MAC randomization** — iPhones and some Android devices use a randomized
  MAC address per network session, making manufacturer lookups unreliable
- **Your own device** — the scanning machine cannot ARP itself, so its MAC
  address shows as (not available)
- **Sleeping devices** — devices in low-power mode may not respond to pings
  and will not appear in results

---

## Usage

**1. Activate the virtual environment:**
```bash
cd ~/network-auditor
source venv/bin/activate
```

**2. Find your subnet:**
```bash
ipconfig getifaddr en0
```
Take the result (e.g. 192.168.3.86) and replace the last number with 0,
then add /24 — giving you 192.168.3.0/24.

**3. Run the scanner:**
```bash
sudo venv/bin/python discover.py 192.168.3.0/24
```

---

## Requirements

- macOS (tested on M1)
- Python 3.x
- nmap — install via Homebrew: `brew install nmap`
- python-nmap — install via pip: `pip install python-nmap`
- prettytable — install via pip: `pip install prettytable`

---

## Roadmap

- [x] Stage 1: Device discovery — ping sweep, ARP, MAC/OUI lookup
- [ ] Stage 2: Port and service scanning
- [ ] Stage 3: Topology inference
- [ ] Stage 4: Audit flags for misconfigurations
- [ ] Stage 5: Web dashboard with visual topology map

---

## Certifications

CompTIA Tech+ | CompTIA Network+ | CCNA (in progress)
