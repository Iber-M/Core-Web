
import json
import urllib.request
import urllib.error
import sys

import os

# CONFIGURATION
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID") # Load from .env
API_URL = "https://api.notion.com/v1/pages"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

print("Preparing payload...")
# Minimal payload
payload = {
    "parent": {"database_id": DATABASE_ID},
    "properties": {
        "Titulo": {"title": [{"text": {"content": "DEBUG TEST POST"}}]}
    }
}
data = json.dumps(payload).encode('utf-8')
print("Payload encoded.")

req = urllib.request.Request(API_URL, data=data, headers=headers, method='POST')
print("Sending request...")

try:
    with urllib.request.urlopen(req, timeout=10) as response:
        print(f"Response Code: {response.status}")
        print(response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
    print(e.read().decode('utf-8'))
except Exception as e:
    print(f"Error: {e}")
