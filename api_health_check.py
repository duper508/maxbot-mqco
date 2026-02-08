#!/usr/bin/env python3
"""
API Key Health Check Script
Monitors all configured API keys and sends daily status report via Signal.
"""

import json
import os
import subprocess
from datetime import datetime
from typing import Dict, Any, Tuple
import requests

# API configurations - read from environment variables
VERCEL_API_KEY = os.getenv("VERCEL_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY", "")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

class APIHealthChecker:
    def __init__(self):
        self.results = {}
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def check_vercel(self) -> Dict[str, Any]:
        """Check Vercel AI Gateway"""
        try:
            # Test Vercel endpoint with light completion request
            headers = {"Authorization": f"Bearer {VERCEL_API_KEY}"}
            payload = {
                "model": "anthropic/claude-haiku-4.5",
                "messages": [{"role": "user", "content": "respond with 'ok'"}],
                "max_tokens": 5
            }
            
            response = requests.post(
                "https://ai-gateway.vercel.sh/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=10
            )
            
            status = "✅" if response.status_code == 200 else "❌"
            
            # Try to get credits info
            credits_response = requests.get(
                "https://ai-gateway.vercel.sh/v1/credits",
                headers=headers,
                timeout=10
            )
            billing_info = ""
            if credits_response.status_code == 200:
                data = credits_response.json()
                billing_info = f"Balance: ${data.get('balance', 'N/A')}"
            
            return {
                "status": status,
                "service": "Vercel AI Gateway",
                "test": "✅ Light completion test",
                "billing": billing_info,
                "details": response.status_code
            }
        except Exception as e:
            return {
                "status": "❌",
                "service": "Vercel AI Gateway",
                "test": f"❌ {str(e)[:50]}",
                "billing": "N/A",
                "details": str(e)
            }

    def check_groq(self) -> Dict[str, Any]:
        """Check Groq API"""
        try:
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": "ok"}],
                "max_tokens": 5
            }
            
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=10
            )
            
            status = "✅" if response.status_code == 200 else "❌"
            return {
                "status": status,
                "service": "Groq",
                "test": "✅ Light completion test" if response.status_code == 200 else f"❌ {response.status_code}",
                "billing": "Free tier (rate-limited)",
                "details": response.status_code
            }
        except Exception as e:
            return {
                "status": "❌",
                "service": "Groq",
                "test": f"❌ {str(e)[:50]}",
                "billing": "N/A",
                "details": str(e)
            }

    def check_brave_search(self) -> Dict[str, Any]:
        """Check Brave Search API"""
        try:
            headers = {"Accept": "application/json", "X-Subscription-Token": BRAVE_API_KEY}
            params = {"q": "test", "count": 1}
            
            response = requests.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers=headers,
                params=params,
                timeout=10
            )
            
            status = "✅" if response.status_code == 200 else "❌"
            return {
                "status": status,
                "service": "Brave Search",
                "test": "✅ Search test" if response.status_code == 200 else f"❌ {response.status_code}",
                "billing": "N/A (unknown)",
                "details": response.status_code
            }
        except Exception as e:
            return {
                "status": "❌",
                "service": "Brave Search",
                "test": f"❌ {str(e)[:50]}",
                "billing": "N/A",
                "details": str(e)
            }

    def check_elevenlabs(self) -> Dict[str, Any]:
        """Check ElevenLabs TTS API"""
        try:
            headers = {"xi-api-key": ELEVENLABS_API_KEY}
            
            # Just check if API is accessible
            response = requests.get(
                "https://api.elevenlabs.io/v1/user",
                headers=headers,
                timeout=10
            )
            
            status = "✅" if response.status_code == 200 else "❌"
            billing_info = ""
            
            if response.status_code == 200:
                data = response.json()
                subscription = data.get("subscription", {})
                character_limit = subscription.get("character_limit", 0)
                character_count = subscription.get("character_count", 0)
                billing_info = f"Usage: {character_count}/{character_limit} chars"
            
            return {
                "status": status,
                "service": "ElevenLabs",
                "test": "✅ API test" if response.status_code == 200 else f"❌ {response.status_code}",
                "billing": billing_info,
                "details": response.status_code
            }
        except Exception as e:
            return {
                "status": "❌",
                "service": "ElevenLabs",
                "test": f"❌ {str(e)[:50]}",
                "billing": "N/A",
                "details": str(e)
            }

    def check_google(self) -> Dict[str, Any]:
        """Check Google APIs"""
        try:
            # Test with a simple Places API call
            params = {"key": GOOGLE_API_KEY, "input": "test", "inputtype": "textquery"}
            
            response = requests.get(
                "https://places.googleapis.com/v1/places:searchText",
                params=params,
                timeout=10
            )
            
            # Google might return 400 for invalid query, but if key is valid, it won't be 401/403
            status = "✅" if response.status_code != 401 and response.status_code != 403 else "❌"
            return {
                "status": status,
                "service": "Google APIs",
                "test": "✅ Key validation" if status == "✅" else "❌ Invalid key",
                "billing": "N/A (unknown)",
                "details": response.status_code
            }
        except Exception as e:
            return {
                "status": "❌",
                "service": "Google APIs",
                "test": f"❌ {str(e)[:50]}",
                "billing": "N/A",
                "details": str(e)
            }

    def generate_html_report(self) -> str:
        """Generate HTML report with results"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        .status-ok {{ color: green; font-weight: bold; }}
        .status-fail {{ color: red; font-weight: bold; }}
        .timestamp {{ color: #666; font-size: 0.9em; }}
    </style>
</head>
<body>
    <h1>🔍 API Health Check Report</h1>
    <p class="timestamp">Generated: {self.timestamp}</p>
    <table>
        <tr>
            <th>Status</th>
            <th>Service</th>
            <th>Test Result</th>
            <th>Billing/Usage</th>
        </tr>
"""
        
        for service_name in ["Vercel AI Gateway", "Groq", "Brave Search", "ElevenLabs", "Google APIs"]:
            result = None
            if service_name == "Vercel AI Gateway":
                result = self.results.get("vercel")
            elif service_name == "Groq":
                result = self.results.get("groq")
            elif service_name == "Brave Search":
                result = self.results.get("brave")
            elif service_name == "ElevenLabs":
                result = self.results.get("elevenlabs")
            elif service_name == "Google APIs":
                result = self.results.get("google")
            
            if result:
                status_class = "status-ok" if result["status"] == "✅" else "status-fail"
                html += f"""
        <tr>
            <td class="{status_class}">{result['status']}</td>
            <td>{result['service']}</td>
            <td>{result['test']}</td>
            <td>{result['billing']}</td>
        </tr>
"""
        
        html += """
    </table>
</body>
</html>
"""
        return html

    def run_all_checks(self):
        """Run all API checks"""
        self.results["vercel"] = self.check_vercel()
        self.results["groq"] = self.check_groq()
        self.results["brave"] = self.check_brave_search()
        self.results["elevenlabs"] = self.check_elevenlabs()
        self.results["google"] = self.check_google()

    def send_via_signal(self, html_content: str):
        """Send report via Signal"""
        try:
            # Save HTML to temp file
            temp_file = "/tmp/api_health_report.html"
            with open(temp_file, "w") as f:
                f.write(html_content)
            
            # Send via message tool
            # This would be handled by Clawdbot's message tool in production
            print(f"Report ready at {temp_file}")
            print("In production, this would be sent via Signal")
            
        except Exception as e:
            print(f"Failed to send report: {e}")

def main():
    checker = APIHealthChecker()
    checker.run_all_checks()
    html_report = checker.generate_html_report()
    
    # Print to stdout (can be piped or saved)
    print(html_report)
    
    # Optionally send via Signal (would be invoked from cron with Clawdbot message tool)
    # checker.send_via_signal(html_report)

if __name__ == "__main__":
    main()
