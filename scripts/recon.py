#!/usr/bin/env python3
"""
recon.py
--------
Simple reconnaissance script using Nmap to discover hosts, open ports,
services, and OS information. Outputs both XML and JSON for further
processing.

Usage:
    python recon.py
    # Edit TARGET_IP or TARGET_RANGE below to suit your lab.
"""

import subprocess
import json
import datetime
import pathlib
import sys

# ----------------- Configuration -----------------
# Set either a single IP or a CIDR range.
TARGET_IP = "127.0.0.1"   # <-- CHANGE TO YOUR LAB TARGET (e.g., "10.0.0.5")
# TARGET_RANGE = "10.0.0.0/24"  # Alternatively, scan a subnet.

# Nmap options: -sS (SYN scan), -sV (service version), -O (OS detection),
# -oX (XML output), -oJ (JSON output via the newer JSON output).
# We'll also add -Pn to skip ping discovery if the host blocks ICMP.
NMAP_OPTS = ["-sS", "-sV", "-O", "-Pn"]

# Output directory
OUT_DIR = pathlib.Path(__file__).resolve().parents[1] / "data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Timestamp for file names
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def run_nmap(target):
    xml_out = OUT_DIR / f"nmap_{TS}.xml"
    json_out = OUT_DIR / f"nmap_{TS}.json"
    cmd = ["nmap"] + NMAP_OPTS + ["-oX", str(xml_out), "-oJ", str(json_out), target]
    print(f"[+] Running Nmap: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[-] Nmap failed: {e}")
        sys.exit(1)
    return xml_out, json_out

def parse_json_to_summary(json_path):
    """Optional: create a human‑readable summary from the JSON output."""
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[-] Could not read JSON: {e}")
        return

    hosts = data.get("hosts", [])
    print("\n=== Nmap Scan Summary ===")
    for host in hosts:
        addr = host.get("address", [{}])[0].get("addr", "unknown")
        status = host.get("status", {}).get("state", "unknown")
        print(f"\nHost: {addr} ({status})")
        # OS
        osmatches = host.get("os", {}).get("osmatch", [])
        if osmatches:
            top_os = osmatches[0].get("name", "unknown")
            print(f"  OS: {top_os}")
        # Ports
        ports = host.get("ports", [])
        if ports:
            print("  Open Ports:")
            for p in ports:
                port_id = p.get("portid")
                proto = p.get("protocol")
                state = p.get("state", {}).get("state")
                service = p.get("service", {})
                sname = service.get("name", "")
                product = service.get("product", "")
                version = service.get("version", "")
                extrainfo = service.get("extrainfo", "")
                print(f"    {port_id}/{proto} {state} {sname} {product} {version} {extrainfo}".strip())
        else:
            print("  No open ports found.")
    print("=========================\n")

def main():
    target = TARGET_IP  # or TARGET_RANGE if you prefer
    if not target:
        print("[-] Please set TARGET_IP or TARGET_RANGE in the script.")
        sys.exit(1)

    xml_out, json_out = run_nmap(target)
    print(f"[+] Nmap XML saved to: {xml_out}")
    print(f"[+] Nmap JSON saved to: {json_out}")
    parse_json_to_summary(json_out)

if __name__ == "__main__":
    main()