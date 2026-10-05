# Web and Network Vulnerability Assessment on Lab Targets

## Project Overview
This project demonstrates a **authorised** vulnerability assessment and penetration testing (VAPT) workflow on intentionally vulnerable lab targets (e.g., Metasploitable, OWASP WebGoat, or a custom test environment). The goal is to showcase:

1. **Reconnaissance** – host discovery, port/service enumeration, OS fingerprinting using **Nmap**.
2. **Vulnerability scanning** – automated scanning with **Nikto** and **OpenVAS** (or `openvas-scanner`).
3. **Manual validation & exploitation** – using **Burp Suite Community** to verify findings (e.g., SQL injection, security misconfiguration, sensitive data exposure).
4. **Risk scoring** – applying **CVSS v3.1** to quantify severity.
5. **Reporting** – generating a structured VAPT report that is consumable by both technical and management audiences.

## Directory Structure
```
web-network-vapt/
│
├─ README.md                 # This file
├─ docs/
│   ├─ nmap-cheatsheet.md    # Common Nmap commands and options
│   ├─ burp-suite-tips.md    # Quick guide to Burp Suite Community features
│   └─ cvss-v3-1-guide.md    # How to calculate CVSS v3.1 base scores
├─ scripts/
│   ├─ recon.py              # Automated Nmap scan + JSON output parser
│   ├─ nikto_scan.sh         # Wrapper to run Nikto on discovered HTTP services
│   ├─ burp_automation.py    # Example of using Burp Suite’s REST API (if Burp Suite Professional is available) or manual steps
│   └─ cvss_calculator.py    # Small helper to compute CVSS v3.1 base score from metric values
├─ data/
│   ├─ sample-nmap.xml       # Example Nmap XML output (for reference)
│   ├─ sample-nikto.txt      # Example Nikto output
│   └─ sample-burp-log.txt   # Example Burp proxy log (requests/responses)
├─ reports/
│   ├─ vapt-report-template.md   # Template for a full VAPT report
│   └─ sample-vapt-report.md     # Example filled‑out report based on lab findings
└─ references/
    ├─ OWASP-Top-10-2021.pdf
    ├─ PTES-Technical-Guidelines.pdf
    └─ NIST-SP-800-115.pdf
```

## How to Reproduce the Work

### Prerequisites
- A lab environment with at least one vulnerable target reachable via IP (e.g., `10.0.0.5`).
- **Nmap** installed (`nmap --version`).
- **Nikto** installed (`nikto -Version`).
- **OpenVAS** (optional) or any other credential‑free scanner.
- **Burp Suite Community** (for manual testing) – ensure the proxy is listening on `127.0.0.1:8080` and your browser is configured to use it.
- Python 3.8+ with `python-nmap` and `requests` (install via `pip install python-nmap requests`).
- Access to a terminal / command prompt.

### Step‑by‑Step

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your‑username>/web-network-vapt.git
   cd web-network-vapt
   ```

2. **Adjust target variables**
   - Edit `scripts/recon.py` and set `TARGET_IP` or `TARGET_RANGE` to your lab target.
   - Edit `scripts/nikto_scan.sh` similarly.

3. **Run reconnaissance**
   ```bash
   python scripts/recon.py
   ```
   - This performs an Nmap SYN scan (`-sS`), service detection (`-sV`), OS fingerprinting (`-O`), and saves XML output to `data/nmap-<timestamp>.xml`.
   - A summary is printed to the console and a JSON version (`data/nmap-<timestamp>.json`) is created for easy parsing.

4. **Run Nikto on discovered HTTP services**
   ```bash
   ./scripts/nikto_scan.sh
   ```
   - The script reads the Nmap JSON, extracts IP:port pairs where service contains "http" or "https", and launches Nikto against each.
   - Output is saved under `data/nikto-<timestamp>.txt`.

5. **Manual validation with Burp Suite**
   - Start Burp Suite, ensure the proxy is running.
   - Use the URLs identified in the Nmap/Nikto output to explore the application.
   - Look for low‑hanging fruit:
        * **SQL Injection** – try `' OR '1'='1` in login fields or URL parameters.
        * **Security Misconfiguration** – check for directory listing, default credentials (`admin/admin`), exposed `.git` or `.env` files.
        * **Sensitive Data Exposure** – watch for clear‑text credentials in HTTP Basic Auth or form submissions.
   - When you find a potential issue, use Burp’s **Repeater** and **Intruder** to confirm and craft a proof‑of‑concept (PoC).

6. **Score findings with CVSS v3.1**
   - For each confirmed vulnerability, fill in the metric values (Attack Vector, Attack Complexity, Privileges Required, User Interaction, Scope, Confidentiality, Integrity, Availability) using the guide in `docs/cvss-v3-1-guide.md`.
   - Run the helper script:
     ```bash
     python scripts/cvss_calculator.py --av L --ac L --pr N --ui N --s U --c H --i H --a H
     ```
   - Record the base score and severity (None, Low, Medium, High, Critical) in your report.

7. **Generate the final VAPT report**
   - Copy `reports/vapt-report-template.md` to `reports/vapt-report-<date>.md`.
   - Populate the sections (Executive Summary, Scope, Methodology, Findings, Conclusion, Appendices) using the data collected in steps 3‑6.
   - Attach raw Nmap/Nikto/Burp logs as appendices.

### Example Workflow (Metasploitable2)
Assuming the target is at `10.0.0.5`:

```bash
# 1. Recon
python scripts/recon.py   # TARGET_IP = "10.0.0.5"
# 2. Nikto
./scripts/nikto_scan.sh
# 3. Manual testing via Burp (explore http://10.0.0.5)
# 4. CVSS example for a root‑shell backdoor via vsftpd 2.3.4:
python scripts/cvss_calculator.py --av N --ac L --pr L --ui N --s U --c H --i H --a H
# => Base Score: 9.8 (Critical)
# 5. Write report
```

## Key Learning Outcomes
- End‑to‑end VAPT process: from reconnaissance to reporting.
- Practical usage of industry‑standard tools (Nmap, Nikto, Burp Suite).
- Ability to translate raw tool output into actionable findings.
- Experience with CVSS v3.1 scoring for consistent risk communication.
- Familiarity with OWASP Top 10 and common web/network misconfigurations.

## Extending the Project
- Integrate with **Metasploit** for automated exploitation (use with caution and only in lab).
- Add credentialed scanning using **OpenVAS** with a test account.
- Develop a small web‑dashboard (Flask/Dash) that displays scan trends over time.
- Containerise the scanning scripts with Docker for reproducible lab setups.

## License
This project is licensed under the MIT License – see the `LICENSE` file for details.

## Acknowledgements
- Metasploitable (Rapid7) – deliberately vulnerable Linux target.
- OWASP WebGoat – intentionally insecure web application.
- The creators of Nmap, Nikto, and Burp Suite.
- PTES and NIST SP 800‑115 for methodological guidance.
