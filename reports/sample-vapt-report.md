# Sample VAPT Report – Metasploitable2 Lab

**Client:** Internal Lab – Metasploitable2  
**Engagement Dates:** 2025-10-05 – 2025-10-05  
**Report Date:** 2025-10-05  
**Prepared By:** Hariom Raut  
**Confidentiality:** Internal Use Only

---

## Executive Summary
A single host (10.0.0.5) was assessed for network and web vulnerabilities. The scan revealed **5** findings: 2 Critical, 2 High, and 1 Medium. The most severe issues are an outdated vsftpd backdoor (CVE‑2011‑2523) and an exposed Git repository that could leak source code. Immediate patching or isolation is advised.

---

## Scope and Objectives
- **In Scope:** 10.0.0.5 (all TCP ports) and the HTTP service on port 80.
- **Out of Scope:** Any other hosts in the 10.0.0.0/24 subnet.
- **Objectives:** Identify exploitable vulnerabilities, verify via manual testing, assign CVSS scores, provide remediation steps.

---

## Methodology
- Recon: `nmap -sS -sV -O -oA recon`.
- Web scan: `nikto -h 10.0.0.5 -p 80`.
- Manual validation: Burp Suite Community (Repeater/Intruder).
- Scoring: CVSS v3.1 using the provided calculator script.

---

## Findings

### Finding 1: vsftpd 2.3.4 Backdoor (CVE‑2011‑2523)
- **Asset:** 10.0.0.5:21/tcp
- **Description:** The vsftpd version 2.3.4 contains a backdoor that allows unauthenticated remote command execution when a username ending with `:)` is supplied.
- **Evidence:** Nmap script `vsftpd_234_backdoor` returned positive output; manual test with FTP client `USER anonymous:)` `PASS anything` yielded shell access.
- **CVSS v3.1:** `AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H → Base Score 9.0 (Critical)`
- **Impact:** Full compromise of the host; attacker can execute arbitrary commands with ftp daemon privileges.
- **Likelihood:** High – service is exposed and default credentials not required.
- **Remediation:** Upgrade vsftpd to a version >2.3.4 or remove the service if not needed. Apply firewall rule to restrict FTP to trusted IPs.
- **References:** CVE‑2011‑2523, https://www.exploit-db.com/exploits/17491

### Finding 2: Exposed Git Repository
- **Asset:** http://10.0.0.5/.git/HEAD
- **Description:** The `.git` directory is publicly accessible, allowing an attacker to clone the repository and obtain source code, configuration files, and potentially credentials.
- **Evidence:** HTTP GET request to `/.git/HEAD` returned `ref: refs/heads/master` (200 OK). Directory listing enabled revealed `objects/`, `refs/`, etc.
- **CVSS v3.1:** `AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N → Base Score 5.3 (Medium)`
- **Impact:** Source code disclosure may reveal business logic, hard‑coded secrets, or lead to further attacks.
- **Likelihood:** Medium – requires knowledge of Git structure but easily exploitable.
- **Remediation:** Ensure `.git` directory is not served by the web server. Move the repository outside the web root or configure `<DirectoryMatch> "^.*/\.git/"` to deny all.
- **References:** OWASP‑A06:2021 – Sensitive Data Exposure

### Finding 3: Directory Listing Enabled
- **Asset:** http://10.0.0.5/images/
- **Description:** The web server is configured to display directory listings when no index file is present.
- **Evidence:** Request to `/images/` returned an HTML index of files (e.g., `logo.png`, `banner.jpg`).
- **CVSS v3.1:** `AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N → Base Score 5.3 (Medium)`
- **Impact:** Information leakage of file names and possibly sensitive backup files.
- **Likelihood:** Medium – trivial to discover.
- **Remediation:** Disable directory listing via `Options -Indexes` in Apache config or equivalent in other web servers.
- **References:** Apache HTTP Server Documentation

### Finding 4: HTTP TRACE Method Enabled (XST Vector)
- **Asset:** http://10.0.0.5/
- **Description:** The HTTP TRACE method is enabled, which can be abused in Cross‑Site Tracing (XST) attacks to steal cookies when combined with certain client‑side vulnerabilities.
- **Evidence:** Nikto reported “OSVDB-877: HTTP TRACE method is active”.
- **CVSS v3.1:** `AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:N/A:N → Base Score 4.0 (Medium)` (User Interaction Required)
- **Impact:** Potential session hijacking if a victim executes a malicious script.
- **Likelihood:** Low – requires chaining with another client‑side flaw.
- **Remediation:** Disable TRACE method (e.g., `TraceEnable Off` in Apache) or restrict via `RewriteRule`.
- **References:** OWASP‑A06:2021 – Sensitive Data Exposure

### Finding 5: Default Credentials – phpMyAdmin (if present)
- **Asset:** http://10.0.0.5/phpmyadmin/
- **Description:** phpMyAdmin interface accessible with default username `root` and empty password.
- **Evidence:** Login attempt succeeded, granting full MySQL control.
- **CVSS v3.1:** `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H → Base Score 9.8 (Critical)`
- **Impact:** Complete database compromise; possible data exfiltration or destruction.
- **Likelihood:** High if the application is installed.
- **Remediation:** Change default credentials, restrict access to trusted IPs, or remove phpMyAdmin if not required.
- **References:** CVE‑2016‑5734 (though default creds are a misconfiguration)

---

## Risk Rating Summary
| Severity | Count |
|----------|-------|
| Critical | 2 |
| High     | 0 |
| Medium   | 3 |
| Low      | 0 |
| Info     | 0 |

---

## Remediation Recommendations
1. **Patch vsftpd** or disable FTP service.
2. **Secure Git** – move `.git` out of web root or deny access via web server config.
3. **Disable directory listing** on all web directories.
4. **Turn off HTTP TRACE** method.
5. **Change default credentials** for any admin panels (phpMyAdmin, etc.).
6. **Apply least privilege** – run services under non‑root accounts.
7. **Regular vulnerability scanning** – schedule weekly Nikto/OpenVAS scans.
8. **Web Application Firewall (WAF)** – consider ModSecurity with OWASP CRS.

---

## Conclusion
The lab host exhibits multiple serious vulnerabilities that would be trivial to exploit in a real‑world scenario. Addressing the items above will raise the security posture significantly. After remediation, a retest is recommended to verify that the issues are resolved.

---

## Appendices
- **Appendix A:** Nmap XML output (`data/sample-nmap.xml`)
- **Appendix B:** Nikto scan log (`data/sample-nikto.txt`)
- **Appendix C:** Burp Suite proxy log (`data/sample-burp-log.txt`)
- **Appendix D:** CVSS calculation worksheet (`scripts/cvss_calculator.py` usage)
- **Appendix E:** Tool versions: Nmap 7.94, Nikto 2.5.0, Burp Suite Community 2025.2

---
*Sample report generated by the Web and Network VAPT project.*