# API Health Check Script

Daily monitoring script that checks the status of all configured API keys and sends a report via Signal at 5 AM.

## Features

- ✅ Tests Vercel AI Gateway (with balance check)
- ✅ Tests Groq API (free tier)
- ✅ Tests Brave Search API
- ✅ Tests ElevenLabs TTS API (with usage stats)
- ✅ Tests Google APIs
- 📊 Generates HTML report with emoji status indicators
- 📱 Sends daily report to Signal at 5 AM
- 💾 Keeps history of reports (7 days)

## Setup

### 1. Create Environment File

Create `~/.api_health_check.env` with your API keys:

```bash
export VERCEL_API_KEY="your-vercel-key"
export GROQ_API_KEY="your-groq-key"
export BRAVE_API_KEY="your-brave-key"
export ELEVENLABS_API_KEY="your-elevenlabs-key"
export GOOGLE_API_KEY="your-google-key"
```

Make it secure:
```bash
chmod 600 ~/.api_health_check.env
```

### 2. Test the Script

```bash
cd /path/to/maxbot-mqco
python3 api_health_check.py
```

Should output an HTML report with all API statuses.

### 3. Setup Cron Job

Add to your crontab:

```bash
crontab -e
```

Add this line (runs daily at 5 AM):

```
0 5 * * * /path/to/maxbot-mqco/run_health_check.sh
```

Or, if you want to run it via Clawdbot's cron, add a cron job through the Clawdbot interface that invokes the script.

## Output

The script generates:
- **HTML Report**: `/tmp/api_health_reports/report_YYYYMMDD_HHMMSS.html`
- **Signal Message**: Sent to your configured Signal account with status summary

## Report Format

| Status | Service | Test Result | Billing/Usage |
|--------|---------|-------------|---------------|
| ✅ | Service Name | ✅ Test passed | Billing info |
| ❌ | Service Name | ❌ Error description | N/A |

## Troubleshooting

### "Failed to send via Signal"
- Check if Clawdbot gateway is running: `clawdbot gateway status`
- Verify Signal is configured in Clawdbot config
- Check Signal account number in the script matches your setup

### API Key not found
- Verify `~/.api_health_check.env` exists and has correct permissions
- Check that API keys are correctly set in the environment file

### High test costs
- Each check uses minimal tokens (~50 tokens per service)
- Monthly cost should be under $0.01 for all checks combined

## Files

- `api_health_check.py` - Main health check logic
- `run_health_check.sh` - Wrapper script for cron/Signal integration
- `README_API_HEALTH_CHECK.md` - This file

## Notes

- Script runs light tests only (not full requests)
- Reports are kept for 7 days in `/tmp/api_health_reports/`
- Environment variables must be exported in `.env` file, not hardcoded
- API keys should never be committed to Git
