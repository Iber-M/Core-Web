
import json
import urllib.request
import urllib.error
import sys

# CONFIGURATION
NOTION_TOKEN = "ntn_rj9457879735z9EOp4381j0VB1ZBG4aAc5L3FtNleGI5t0"
DATABASE_ID = "2fd0385f-9445-80ed-b5cf-fb9cecc1013b"
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
