
import json
import time
import subprocess
import os
import sys

# CONFIGURATION
# Load from environment variables for security
# Ensure you have a .env file or export these variables
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID", "2fd0385f-9445-80ed-b5cf-fb9cecc1013b") # Default or Env
PAYLOAD_FILE = "scripts/notion_import_payload.json"
API_URL = "https://api.notion.com/v1/pages"

def import_posts():
    if not NOTION_TOKEN:
        print("Error: NOTION_TOKEN env var not set. Please create a .env file or export it.")
        return

    try:
        with open(PAYLOAD_FILE, 'r', encoding='utf-8') as f:
            posts = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {PAYLOAD_FILE}")
        return

    print(f"Starting import of {len(posts)} posts via cURL...")
    
    success_count = 0
    error_count = 0
    
    for i, post_data in enumerate(posts):
        # Construct payload
        payload = {
            "parent": {"database_id": DATABASE_ID},
            "properties": post_data["properties"],
            "children": post_data["children"]
        }
        
        # Write temp file for curl
        temp_filename = f"temp_payload_{i}.json"
        with open(temp_filename, 'w', encoding='utf-8') as f:
            json.dump(payload, f)
            
        # Build curl command
        # -s = silent (no progress bar)
        # -S = show error
        # -w = write out HTTP code
        cmd = [
            "curl", "-s", "-S",
            "-X", "POST",
            API_URL,
            "-H", f"Authorization: Bearer {NOTION_TOKEN}",
            "-H", "Content-Type: application/json",
            "-H", "Notion-Version: 2022-06-28",
            "-d", f"@{temp_filename}"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Basic check: if output contains "object":"page" it was likely successful
            # Notion returns the object on success.
            # On error it returns "object":"error"
            
            if '"object":"page"' in result.stdout:
                title = post_data['properties']['Titulo']['title'][0]['text']['content']
                print(f"[{i+1}/{len(posts)}] ✅ Imported: {title}")
                success_count += 1
            else:
                print(f"[{i+1}/{len(posts)}] ❌ Failed: {result.stdout[:200]}...")
                error_count += 1
                
        except Exception as e:
            print(f"[{i+1}/{len(posts)}] ❌ Exec Error: {str(e)}")
            error_count += 1
        finally:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
            
        # Respect rate limits
        time.sleep(0.3)
        
    print("\n========================================")
    print(f"Import Finished.")
    print(f"Success: {success_count}")
    print(f"Failed: {error_count}")
    print("========================================")

if __name__ == "__main__":
    import_posts()
