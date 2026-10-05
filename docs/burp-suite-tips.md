# Burp Suite Community – Quick Tips for Manual Testing

## 1. Setting Up the Proxy
1. Start Burp Suite → Proxy → Intercept is **off** (so traffic flows freely).
2. Configure your browser (Firefox/Chrome) to use Burp as a proxy:
   - HTTP Proxy: `127.0.0.1`
   - Port: `8080` (default)
   - Enable “Use this proxy server for all protocols”.
3. Install Burp’s CA certificate in the browser to intercept HTTPS traffic:
   - Proxy → Options → Import/export CA certificate → “Certificate in DER format” → Save to desktop.
   - In browser, import the DER certificate under Authorities and trust it for identifying websites.

## 2. Core Tabs for VAPT
| Tab | Purpose | Typical Use |
|-----|---------|-------------|
| **Target** | Site map and scope | Define scope (add URL patterns) to limit scanning/logging. |
| **Proxy** | Intercept & view requests/responses | View raw HTTP, edit and resend (via Repeater). |
| **Repeater** | Manually tweak and resend a single request | Test parameter changes, inject payloads. |
| **Intruder** | Automated attacks (e.g., brute force, fuzzing) | Payload positions, fuzzing lists, thread control. |
| **Scanner** (Professional only) | Automated active scanning | Not available in Community; replace with manual checks or external scanners (Nikto, Zap). |
| **Decoder** | Encode/decode data | URL‑encode, base64, hash, etc. |
| **Comparer** | Compare two requests/responses | Spot differences (e.g., before/after auth). |
| **Sequencer** | Analyse randomness (e.g., session tokens) | Collect tokens, assess entropy. |
| **Extensions** (via BApp Store) | Add community‑built tools | e.g., JSONWizard, Retire.js, AutoRepeater. |

## 3. Common Workflow for Finding Vulnerabilities
1. **Browse** the application manually while Burp captures traffic.
2. **Right‑click** an interesting request → “Send to Repeater”.
3. In Repeater, modify parameters:
   - Try SQLi payloads: `' OR '1'='1`, `' UNION SELECT NULL,@@version,--`.
   - Try XSS payloads: `<script>alert(1)</script>`.
   - Try path traversal: `../../etc/passwd`.
4. Click **Go** to send the modified request; examine the response for signs of success (error messages, data leakage, status code changes).
5. If you suspect a vulnerability, send the request to **Intruder**:
   - Clear `$` position markers.
   - Highlight the parameter to fuzz.
   - Choose payload set (e.g., OWASP XSS wordlist).
   - Launch attack and grep for interesting responses (different length, status code, presence of certain strings).
6. For **authentication/testing**:
   - Use **Sequencer** to collect session tokens and evaluate randomness.
   - Use **Repeater** to attempt brute force on login (with Intruder’s “Sniper” attack using a username/password list).
7. **Logging & Reporting**:
   - Use Proxy → History to export selected requests/responses (right‑click → “Export selected items”) → Save as XML or HTML for inclusion in your report.
   - Use the **Site map** (Target tab) to export scope as XML.

## 4. Helpful Shortcuts
| Action | Shortcut |
|--------|----------|
| Send to Repeater | `Ctrl+R` |
| Send to Intruder | `Ctrl+I` |
| Send to Scanner (Professional) | `Ctrl+U` |
| Add to Scope | `Ctrl+D` |
| Clear Intercept | `Ctrl+L` |
| Start/Stop Intruder | `Ctrl+Shift+L` |
| Show/Hide Inspector | `Ctrl+Shift+I` |

## 5. Extending Functionality (Community Edition)
Although the Community edition lacks the automated Scanner, you can:
- Install **OWASP ZAP** as a complementary passive scanner.
- Use **Nikto** from the command line and import results into Burp via the **Scanner** tab (if you have Professional) or just attach as raw logs.
- Write custom **Burp Extensions** in Java (requires Burp Suite Professional for extending UI) or use **Python-based** tools that interact via the REST API (available in Professional). For Community, stick to manual techniques and external CLI tools.

## 6. Example: Detecting SQLi with Burp Repeater
1. Locate a login POST request: `POST /login.php` with parameters `username` & `password`.
2. Send to Repeater.
3. Change `username` field to: `' OR '1'='1` --`.
4. Keep password as anything (or blank).
5. Press Go.
6. Observe response:
   - If you see a welcome page or a session cookie set, likely SQLi succeeded.
   - If you see an error like “SQL syntax…”, it’s still indicative; try a different payload.

## 7. Example: Testing for Directory Listing
1. Request `GET /images/` (or any folder).
2. In Repeater, ensure no query string.
3. Look at response body:
   - If you see an index of files (e.g., “Index of /images”), directory listing is enabled.
   - Recommend disabling directory listing via web server configuration.

## References
- Burp Suite Documentation: https://portswigger.net/burp/documentation/desktop/getting-started
- Burp Suite Community Edition Features: https://portswigger.net/burp/communitydownload
- OWASP Testing Guide v4: https://owasp.org/www-project-testing-guide/
