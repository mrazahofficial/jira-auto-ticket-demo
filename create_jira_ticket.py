import os
import requests
import sys

# ==============================
# Environment Variables & Sanitization
# ==============================

# We use .strip() to remove accidental spaces or newlines from GitHub Secrets
JIRA_URL = os.environ.get("JIRA_URL", "").strip()
EMAIL = os.environ.get("JIRA_EMAIL", "").strip()
API_TOKEN = os.environ.get("JIRA_API_TOKEN", "").strip()
PROJECT_KEY = os.environ.get("JIRA_PROJECT", "").strip()
SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK", "").strip()

# Fix the URL protocol if it's missing or malformed
if JIRA_URL and not JIRA_URL.startswith("http"):
    JIRA_URL = f"https://{JIRA_URL}"

# Remove trailing slash to prevent double-slashes in the final URL
JIRA_URL = JIRA_URL.rstrip("/")

# ==============================
# Validation Check
# ==============================

required_vars = [JIRA_URL, EMAIL, API_TOKEN, PROJECT_KEY]

if not all(required_vars):
    print("❌ Missing required environment variables.")
    # Debug print to see which one is missing (without showing secrets)
    print(f"JIRA_URL present: {bool(JIRA_URL)}")
    print(f"EMAIL present: {bool(EMAIL)}")
    print(f"TOKEN present: {bool(API_TOKEN)}")
    print(f"PROJECT present: {bool(PROJECT_KEY)}")
    sys.exit(1)

# ==============================
# Create Jira Ticket
# ==============================

def create_ticket():
    url = f"{JIRA_URL}/rest/api/3/issue"
    auth = (EMAIL, API_TOKEN)
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    payload = {
        "fields": {
            "project": {"key": PROJECT_KEY},
            "summary": "🚨 Security Vulnerability Detected",
            "description": {
                "type": "doc", "version": 1, 
                "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Scan failed."}]}]
            },
            "issuetype": {"name": "Task"} # Verify this is 'Task' in your Jira!
        }
    }

    print(f"🚀 Attempting to connect to: {url}")
    try:
        response = requests.post(url, json=payload, headers=headers, auth=auth)
        print("Jira Status Code:", response.status_code)
        
        if response.status_code == 201:
            print("✅ Success! Ticket created.")
        else:
            # THIS IS THE FIX: Print the exact reason from Jira
            print("❌ Jira Error Response:", response.text)
            sys.exit(1)
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        sys.exit(1)
