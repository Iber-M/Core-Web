
import json
import time
import subprocess
import os
import sys

# CONFIGURATION
NOTION_TOKEN = "ntn_rj9457879735z9EOp4381j0VB1ZBG4aAc5L3FtNleGI5t0"
DATABASE_ID = "2fd0385f-9445-80ed-b5cf-fb9cecc1013b"
PAYLOAD_FILE = "scripts/notion_import_payload.json"
API_URL_PAGES = "https://api.notion.com/v1/pages"
API_URL_BLOCKS = "https://api.notion.com/v1/blocks"

def chunk_blocks(blocks, size=100):
    for i in range(0, len(blocks), size):
        yield blocks[i:i + size]

def fix_posts():
    try:
        with open(PAYLOAD_FILE, 'r', encoding='utf-8') as f:
            posts = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {PAYLOAD_FILE}")
        return

    print(f"Scanning {len(posts)} posts for long content (>100 blocks)...")
    
    fixed_count = 0
    
    for i, post_data in enumerate(posts):
        children = post_data["children"]
        if len(children) <= 100:
            continue # Skip non-problematic posts
            
        title = post_data['properties']['Titulo']['title'][0]['text']['content']
        print(f"[{i+1}] Found Long Post ({len(children)} blocks): {title}")
        
        # Split blocks
        chunks = list(chunk_blocks(children, 100))
        first_chunk = chunks[0]
        remaining_chunks = chunks[1:]
        
        # 1. Create Page with First Chunk
        payload = {
            "parent": {"database_id": DATABASE_ID},
            "properties": post_data["properties"],
            "children": first_chunk
        }
        
        temp_filename = f"temp_fix_{i}.json"
        with open(temp_filename, 'w', encoding='utf-8') as f:
            json.dump(payload, f)
            
        print(f"   Creating page base...")
        cmd = [
            "curl", "-s", "-S",
            "-X", "POST",
            API_URL_PAGES,
            "-H", f"Authorization: Bearer {NOTION_TOKEN}",
            "-H", "Content-Type: application/json",
            "-H", "Notion-Version: 2022-06-28",
            "-d", f"@{temp_filename}"
        ]
        
        page_id = None
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            response = json.loads(result.stdout)
            
            if "id" in response and "object" in response and response["object"] == "page":
                page_id = response["id"]
                print(f"   ✅ Page Created: {page_id}")
            else:
                print(f"   ❌ Failed to create page: {result.stdout[:200]}")
                continue
                
        finally:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
        
        if not page_id:
            continue
            
        # 2. Append Remaining Chunks
        for idx, chunk in enumerate(remaining_chunks):
            print(f"   Appending chunk {idx+2}/{len(chunks)}...")
            
            append_payload = {
                "children": chunk
            }
            
            with open(temp_filename, 'w', encoding='utf-8') as f:
                json.dump(append_payload, f)
                
            cmd_append = [
                "curl", "-s", "-S",
                "-X", "PATCH",
                f"{API_URL_BLOCKS}/{page_id}/children",
                "-H", f"Authorization: Bearer {NOTION_TOKEN}",
                "-H", "Content-Type: application/json",
                "-H", "Notion-Version: 2022-06-28",
                "-d", f"@{temp_filename}"
            ]
            
            try:
                res_append = subprocess.run(cmd_append, capture_output=True, text=True)
                if '"object":"list"' in res_append.stdout or '"results":' in res_append.stdout:
                    print(f"   ✅ Chunk {idx+2} appended.")
                else:
                    print(f"   ❌ Chunk {idx+2} failed: {res_append.stdout[:200]}")
            finally:
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)
                    
            time.sleep(0.3)
            
        fixed_count += 1
        print(f"   🎉 Fully Fixed: {title}")
        print("--------------------------------")
        
    print(f"\nCorrection Process Finished. Fixed {fixed_count} long posts.")

if __name__ == "__main__":
    fix_posts()
