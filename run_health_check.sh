#!/bin/bash
# Wrapper script to run API health check and send via Signal
# Scheduled to run daily at 5 AM via cron

set -e

# Source environment variables from .env file (not committed to repo)
# Create ~/.api_health_check.env with your API keys
if [ -f ~/.api_health_check.env ]; then
    set -a
    source ~/.api_health_check.env
    set +a
else
    echo "Error: ~/.api_health_check.env not found. See README.md for setup instructions."
    exit 1
fi

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPORT_DIR="/tmp/api_health_reports"
mkdir -p "$REPORT_DIR"

# Run health check
REPORT_FILE="$REPORT_DIR/report_$(date +%Y%m%d_%H%M%S).html"
python3 "$SCRIPT_DIR/api_health_check.py" > "$REPORT_FILE"

# Send via Clawdbot message tool (via gateway)
# Usage: clawdbot message send --to <signal_number> --channel signal --message <file>
# Since we're sending HTML, we might want to convert to text or just send via the message tool

# Extract text summary from HTML for Signal
SUMMARY=$(python3 << 'EOF'
import re
with open("$REPORT_FILE", 'r') as f:
    content = f.read()
    # Extract status rows
    statuses = re.findall(r'<td class="status-(ok|fail)">([^<]+)</td>\s*<td>([^<]+)</td>', content)
    print("🔍 API Health Check - $(date +%Y-%m-%d)")
    for status_class, emoji, service in statuses:
        print(f"  {emoji} {service}")
EOF
)

# Send to Signal (via Clawdbot)
# Note: This requires Clawdbot to be running and configured with Signal
# Adjust the target number as needed (-13033952041 is the configured Signal account)
clawdbot message send \
  --channel signal \
  --target "+13033952041" \
  --message "API Health Report\n\n$(cat $REPORT_FILE)" \
  2>/dev/null || echo "Failed to send via Signal (Clawdbot may not be running)"

# Keep recent reports
find "$REPORT_DIR" -type f -name "*.html" -mtime +7 -delete

echo "Health check complete. Report saved to $REPORT_FILE"
