#!/usr/bin/env python3
""" Check Claude API Credits
This script checks your available credits and usage for the Anthropic Claude API.
"""
import requests
import json
import os
import sys
from datetime import datetime
# Get API key from environment variable
API_KEY = os.environ.get('ANTHROPIC_API_KEY')
if not API_KEY:
    print("Error: ANTHROPIC_API_KEY environment variable not set")
    print("Set it with: export ANTHROPIC_API_KEY='your-api-key-here'")
    sys.exit(1)
# API endpoint for usage/billing info
# Note: Anthropic's API doesn't have a direct credits endpoint in the public API
# You'll need to check the Console at https://console.anthropic.com/settings/usage
# or use the organization API if you have access
def check_api_key_validity():
    """Test if the API key is valid by making a minimal API call"""
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    data = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 1,
        "messages": [
            {"role": "user", "content": "Hi"}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print("✓ API Key is valid")
            return True
        elif response.status_code == 401:
            print("✗ API Key is invalid or expired")
            return False
        else:
            print(f"⚠ Unexpected response: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"✗ Error making API call: {e}")
        return False
def get_organization_info():
    """Get organization information if available"""
    # This endpoint may require organization-level API access
    url = "https://api.anthropic.com/v1/organizations"
    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        return None
def main():
    print("=" * 60)
    print("Claude API Credits Checker")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    # Check if API key is valid
    if check_api_key_validity():
        print()
        print("Note: Anthropic's public API doesn't expose credits/billing info directly.")
        print("To check your actual credits and usage, please visit:")
        print("https://console.anthropic.com/settings/usage")
        print()
        print("For programmatic access to billing info, you may need:")
        print("- Organization-level API access")
        print("- Contact Anthropic support for billing API access")
        # Try to get org info (may not work with standard API keys)
        org_info = get_organization_info()
        if org_info:
            print()
            print("Organization Information:")
            print(json.dumps(org_info, indent=2))
            print()
            print("=" * 60)
if __name__ == "__main__":
    main()