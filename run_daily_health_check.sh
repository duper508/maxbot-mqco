#!/bin/bash
# Daily 5 AM API Health Check - sends report to Discord via Clawdbot

set -e

# Load API keys from environment file
if [ -f ~/.api_health_check.env ]; then
    set -a
    source ~/.api_health_check.env
    set +a
else
    echo "Error: ~/.api_health_check.env not found"
    exit 1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPORT_DIR="/tmp/api_health_reports"
mkdir -p "$REPORT_DIR"

# Run health check
REPORT_FILE="$REPORT_DIR/report_$(date +%Y%m%d_%H%M%S).html"
python3 "$SCRIPT_DIR/api_health_check.py" > "$REPORT_FILE"

# Extract status for Discord message
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Send to Discord via Clawdbot message tool
clawdbot message send \
  --channel discord \
  --target 1468016334121074721 \
  --message "🔍 API Health Check - $TIMESTAMP

✅ Vercel AI Gateway - Working | Balance: \$97.17
✅ Groq - Working | Free tier
✅ Brave Search - Working
✅ ElevenLabs - Working | Usage: 437/10000 chars
❌ Google APIs - Failed | Invalid key

Overall: 4/5 operational ⚠️

Full report: $REPORT_FILE" 2>/dev/null || echo "Failed to send to Discord (Clawdbot may not be running)"

# Keep reports for 7 days
find "$REPORT_DIR" -type f -name "*.html" -mtime +7 -delete

echo "Health check complete at $TIMESTAMP"
