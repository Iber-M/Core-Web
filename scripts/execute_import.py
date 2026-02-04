
import json
import time
import urllib.request
import urllib.error
import sys

# CONFIGURATION
NOTION_TOKEN = "ntn_rj9457879735z9EOp4381j0VB1ZBG4aAc5L3FtNleGI5t0"
DATABASE_ID = "2fd0385f-9445-80ed-b5cf-fb9cecc1013b"
PAYLOAD_FILE = "scripts/notion_import_payload.json"
API_URL = "https://api.notion.com/v1/pages"

def import_posts():
    try:
        with open(PAYLOAD_FILE, 'r', encoding='utf-8') as f:
            posts = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {PAYLOAD_FILE}")
        return

    print(f"Starting import of {len(posts)} posts to Notion database {DATABASE_ID}...")
    
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    success_count = 0
    error_count = 0
    
    for i, post_data in enumerate(posts):
        # Add database parent
        payload = {
            "parent": {"database_id": DATABASE_ID},
            "properties": post_data["properties"],
            "children": post_data["children"]
        }
        
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(API_URL, data=data, headers=headers, method='POST')
        
        try:
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    print(f"[{i+1}/{len(posts)}] ✅ Imported: {post_data['properties']['Titulo']['title'][0]['text']['content']}")
                    success_count += 1
                else:
                    print(f"[{i+1}/{len(posts)}] ❓ Status {response.status}")
                    
        except urllib.error.HTTPError as e:
            error_message = e.read().decode('utf-8')
            print(f"[{i+1}/{len(posts)}] ❌ Failed: {e.code} - {error_message}")
            error_count += 1
        except Exception as e:
            print(f"[{i+1}/{len(posts)}] ❌ Error: {str(e)}")
            error_count += 1
            
        # Respect rate limits slightly
        time.sleep(0.4)
        
    print("\n========================================")
    print(f"Import Finished.")
    print(f"Success: {success_count}")
    print(f"Failed: {error_count}")
    print("========================================")

if __name__ == "__main__":
    import_posts()
