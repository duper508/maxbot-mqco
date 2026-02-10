#!/usr/bin/env python3
"""
Check for API health report and send to Discord if fresh.
Called via heartbeat or manually.
"""
import os
import json
import time
from pathlib import Path

SUMMARY_FILE = "/tmp/api_health_reports/latest_summary.txt"
SENT_FILE = "/tmp/api_health_reports/.sent_timestamps"
CHANNEL = "1468016334121074721"
MAX_AGE_MINUTES = 90

def read_summary():
    """Read the latest summary file."""
    if not Path(SUMMARY_FILE).exists():
        return None
    
    summary = {}
    with open(SUMMARY_FILE) as f:
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                summary[key] = value
    return summary

def get_sent_timestamps():
    """Load timestamps of already-sent reports."""
    if not Path(SENT_FILE).exists():
        return set()
    
    with open(SENT_FILE) as f:
        return set(json.load(f))

def save_sent_timestamp(timestamp):
    """Save sent report timestamp."""
    sent = get_sent_timestamps()
    sent.add(timestamp)
    Path(SENT_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(SENT_FILE, "w") as f:
        json.dump(list(sent), f)

def is_fresh(timestamp_str):
    """Check if report is fresh (within MAX_AGE_MINUTES)."""
    try:
        from datetime import datetime
        report_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        age_minutes = (datetime.now() - report_time).total_seconds() / 60
        return age_minutes < MAX_AGE_MINUTES
    except:
        return False

def main():
    summary = read_summary()
    if not summary:
        print("No health check report found.")
        return
    
    timestamp = summary.get("TIMESTAMP")
    if not timestamp or timestamp in get_sent_timestamps():
        print(f"Report already sent or timestamp missing: {timestamp}")
        return
    
    if not is_fresh(timestamp):
        print(f"Report too old ({timestamp}), skipping.")
        return
    
    # Format message for Discord
    message = f"""🔍 **API Health Check** - {timestamp}

✅ Working: {summary.get('OPERATING', 'N/A')}
❌ Failed: {summary.get('FAILED', 'N/A')}

Report: {summary.get('REPORT_FILE', 'N/A')}"""
    
    # This would be called from Clawdbot context where message tool works
    # For now, just print the message that should be sent
    print(f"\n[SEND TO DISCORD {CHANNEL}]")
    print(message)
    print(f"[END MESSAGE]\n")
    
    # Mark as sent
    save_sent_timestamp(timestamp)
    print(f"Report marked as sent: {timestamp}")

if __name__ == "__main__":
    main()
