import os
import requests
import sys

# ==============================
# Environment Variables
# ==============================

JIRA_URL = os.environ.get("JIRA_URL")
EMAIL = os.environ.get("JIRA_EMAIL")
API_TOKEN = os.environ.get("JIRA_API_TOKEN")
PROJECT_KEY = os.environ.get("JIRA_PROJECT")
SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK")

# ==============================
# Validation Check
# ==============================

required_vars = [JIRA_URL, EMAIL, API_TOKEN, PROJECT_KEY]

if not all(required_vars):
    print("❌ Missing required environment variables.")
    sys.exit(1)

# ==============================
# Create Jira Ticket
# ==============================

def create_ticket():

    url = f"{JIRA_URL}/rest/api/3/issue"
    auth = (EMAIL, API_TOKEN)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Simulated severity (for demo / case study)
    priority = "High"

    payload = {
        "fields": {
            "project": {
                "key": PROJECT_KEY
            },
            "summary": "🚨 Security Vulnerability Detected via CI",
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": "Automated CI scan detected a critical vulnerability in the repository. Immediate review is required by the IT Security Team."
                            }
                        ]
                    }
                ]
            },
            "issuetype": {
                "name": "Task"
            },
            "priority": {
                "name": priority
            }
        }
    }

    print("🚀 Creating Jira ticket...")
    response = requests.post(url, json=payload, headers=headers, auth=auth)

    print("Jira Status Code:", response.status_code)
    print("Jira Response:", response.text)

    # ==============================
    # Slack Notification
    # ==============================

    if response.status_code == 201:

        issue_key = response.json()["key"]
        jira_link = f"{JIRA_URL}/browse/{issue_key}"

        print(f"✅ Ticket Created: {issue_key}")

        if SLACK_WEBHOOK:

            slack_message = {
                "text": f"""
🚨 *Security Vulnerability Detected*

• Ticket: {issue_key}
• Severity: {priority}
• Project: {PROJECT_KEY}

🔗 View in Jira:
{jira_link}

Assigned to: IT Support Team
"""
            }

            print("📢 Sending Slack notification...")

            slack_response = requests.post(SLACK_WEBHOOK, json=slack_message)

            print("Slack Status Code:", slack_response.status_code)
            print("Slack Response:", slack_response.text)

        else:
            print("⚠ SLACK_WEBHOOK not configured. Skipping Slack notification.")

    else:
        print("❌ Failed to create Jira ticket.")
        sys.exit(1)


# ==============================
# Run Script
# ==============================

if __name__ == "__main__":
    create_ticket()
