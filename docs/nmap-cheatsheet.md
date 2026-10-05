# Nmap Cheat Sheet – Common Commands for VAPT

## 1. Host Discovery
```bash
# Ping scan (no port scan)
nmap -sn 10.0.0.0/24

# List scan (just list IPs that respond to ping)
nmap -sL 10.0.0.0/24
```

## 2. Port Scanning
```bash
# SYN scan (stealth, default if you have privileges)
nmap -sS -p- 10.0.0.5

# Full TCP connect scan (no privileged needed)
nmap -sT -p- 10.0.0.5

# UDP scan (top 100 ports)
nmap -sU --top-ports 100 10.0.0.5
```

## 3. Service & Version Detection
```bash
# Detect service versions on open TCP ports
nmap -sV -p 80,443,8080 10.0.0.5

# Aggressive version detection + script scanning
nmap -A -p- 10.0.0.5   # -A = -O (OS) + -sV + -sC (default scripts) + traceroute
```

## 4. OS Fingerprinting
```bash
nmap -O 10.0.0.5
# Requires root/administrator privileges for best accuracy.
```

## 5. Script Scanning (NSE)
```bash
# Run default scripts against discovered services
nmap -sC -p- 10.0.0.5

# Run specific scripts (e.g., vuln, http-* )
nmap --script vuln -p- 10.0.0.5
nmap --script "http-*" -p 80,443 10.0.0.5
```

## 6. Output Formats
```bash
# Normal (human‑readable)
nmap -oN scan.txt 10.0.0.5

# XML (good for further processing)
nmap -oX scan.xml 10.0.0.5

# JSON (via xslt or python‑nmap)
nmap -oJ scan.json 10.0.0.5

# Grep‑able
nmap -oG scan.gnmap 10.0.0.5
```

## 7. Performance Tuning
```bash
# Increase speed (lower accuracy)
nmap -T4 -p- 10.0.0.5

# Be very slow and stealthy
nmap -T0 -p- 10.0.0.5

# Limit parallelism
nmap --max-retries 1 --max-rate 100 -p- 10.0.0.5
```

## 8. Common VAPT One‑Liners
```bash
# Quick external‑facing sweep (top 1000 ports)
nmap -sS --top-ports 1000 -T4 <target>

# Internal network discovery + service enumeration
nmap -sS -sV -O -oA internal_scan 10.0.0.0/24

# Scan for common web‑app misconfigurations
nmap --script http-enum,http-methods,http-passwd -p 80,443 <target>
```

## References
- Official Nmap Reference Guide: https://nmap.org/book/man.html
- NSE Script Library: https://nmap.org/nsedoc/