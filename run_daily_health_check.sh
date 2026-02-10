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

# Extract status counts and write to summary file
OPERATING=$(grep -o "status-ok" "$REPORT_FILE" | wc -l)
FAILED=$(grep -o "status-fail" "$REPORT_FILE" | wc -l)

SUMMARY_FILE="/tmp/api_health_reports/latest_summary.txt"
cat > "$SUMMARY_FILE" << SUMMARY
TIMESTAMP=$TIMESTAMP
OPERATING=$OPERATING
FAILED=$FAILED
REPORT_FILE=$REPORT_FILE
SUMMARY

echo "Health check report ready at $REPORT_FILE"

# Keep reports for 7 days
find "$REPORT_DIR" -type f -name "*.html" -mtime +7 -delete

echo "Health check complete at $TIMESTAMP"
