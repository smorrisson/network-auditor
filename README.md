# Network Auditor

A Python-based network scanning tool built while studying for CCNA.

## What it does
Scans a local subnet and discovers all active devices,
displaying their IP address, MAC address, and hostname in a
formatted table.

## What I learned
- Applying CIDR notation to define scan targets
- How ARP operates at Layer 2 to resolve MAC addresses
- Why reverse DNS lookups sometimes fail on local networks
- Using Python virtual environments for clean dependency management

## Usage
1. Activate the virtual environment:
   source venv/bin/activate

2. Run the scanner:
   sudo venv/bin/python discover.py 192.168.x.0/24

## Requirements
- Python 3.x
- nmap (install via Homebrew: brew install nmap)
- python-nmap
- prettytable

## Roadmap
- Stage 2: Port & service scanning
- Stage 3: Topology inference
- Stage 4: Audit flags for misconfigs
- Stage 5: Web dashboard

## Certifications
CompTIA Tech+ | CompTIA Network+ | CCNA (in progress)
