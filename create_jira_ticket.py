import requests
import os
import json

JIRA_URL = os.environ["JIRA_URL"]
EMAIL = os.environ["JIRA_EMAIL"]
API_TOKEN = os.environ["JIRA_API_TOKEN"]
PROJECT_KEY = os.environ["JIRA_PROJECT"]

def create_ticket():
    url = f"{JIRA_URL}/rest/api/3/issue"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    auth = (EMAIL, API_TOKEN)

    payload = {
        "fields": {
            "project": {
                "key": PROJECT_KEY
            },
            "summary": "🚨 Security Issue Detected via CI Pipeline",
            "description": "Automated scan detected a potential vulnerability.",
            "issuetype": {
                "name": "Task"
            }
        }
    }

    response = requests.post(url, json=payload, headers=headers, auth=auth)

    print("Status:", response.status_code)
    print(response.text)

if __name__ == "__main__":
    create_ticket()
