#!/usr/bin/env bash
#
# nikto_scan.sh
# -------------
# Wrapper to run Nikto against HTTP/HTTPS services discovered by the
# recon.py script (which produces a JSON file). The script reads the
# most recent Nmap JSON, extracts IP:port pairs where the service name
# contains "http" or "https", and launches Nikto against each.
#
# Requirements:
#   - nikto (https://cirt.net/Nikto2)
#   - jq (for JSON parsing) – install via your package manager.
#   - The recon.py script must have been run recently so that
#     data/nmap_*.json exists.
#
# Usage:
#   ./nikto_scan.sh
#   # Optionally specify a different JSON file:
#   #   ./nikto_scan.sh /path/to/old_scan.json

set -euo pipefail

# ----------------- Configuration -----------------
# Directory where recon.py stores its output
DATA_DIR="$(dirname "$0")/../data"

# If an argument is given, use that as the JSON file; otherwise pick the newest.
if [ $# -eq 0 ]; then
    JSON_FILE=$(ls -t "$DATA_DIR"/nmap_*.json 2>/dev/null | head -n1)
else
    JSON_FILE="$1"
fi

if [ -z "$JSON_FILE" ] || [ ! -f "$JSON_FILE" ]; then
    echo "Error: No Nmap JSON file found in $DATA_DIR"
    echo "Run recon.py first or provide a valid JSON file path."
    exit 1
fi

echo "[+] Using Nmap JSON: $JSON_FILE"

# Create output directory for Nikto results
NIKTO_OUT_DIR="$DATA_DIR/nikto_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$NIKTO_OUT_DIR"

# Extract host:port where service contains http or https
# jq query: .hosts[].ports[] | select(.service.name | test("http"; "i")) | .host.addr + ":" + .portid
# Note: The JSON structure from nmap -oJ is slightly different; we rely on python-nmap's output.
# For simplicity, we'll use a small Python one‑liner to do the extraction.

PYTHON_CMD="import sys,json;data=json.load(open(sys.argv[1]));"
PYTHON_CMD+="[h['addr'] + ':' + str(p['portid']) for h in data.get('hosts',[]) "
PYTHON_CMD+="for p in h.get('ports',[]) if p.get('state',{}).get('state')=='open' "
PYTHON_CMD+="and 'http' in p.get('service',{}).get('name','').lower()]"

TARGETS=$(python3 -c "$PYTHON_CMD" "$JSON_FILE" | tr '\n' ' ')

if [ -z "$TARGETS" ]; then
    echo "[-] No HTTP/HTTPS services discovered in the Nmap scan."
    exit 0
fi

echo "[+] Targets for Nikto: $TARGETS"

# Loop over each target and run Nikto
for TARGET in $TARGETS; do
    # Split into host and port
    HOST="${TARGET%:*}"
    PORT="${TARGET#*:}"
    OUTFILE="$NIKTO_OUT_DIR/nikto_${HOST}_${PORT}.txt"
    echo "[+] Scanning $HOST:$PORT with Nikto -> $OUTFILE"
    nikto -h "$HOST" -p "$PORT" -Format txt -output "$OUTFILE" -Tuning x 2>&1 | tee -a "$OUTFILE"
done

echo "[+] Nikto scans completed. Results in: $NIKTO_OUT_DIR"
echo "[+] Remember to manually verify any findings and consider false positives."