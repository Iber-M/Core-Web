
import os
import json
import urllib.request
import urllib.error
from collections import defaultdict
from datetime import datetime
import time

# Configuration
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID", "2fd0385f-9445-81cc-8703-f8174967321b")
API_URL = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
PAGE_URL_BASE = "https://api.notion.com/v1/pages"

def get_all_posts():
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    all_posts = []
    has_more = True
    next_cursor = None
    
    print("Fetching all posts to analyze...")
    
    while has_more:
        data_payload = {"page_size": 100}
        if next_cursor:
            data_payload["start_cursor"] = next_cursor
            
        req = urllib.request.Request(API_URL, data=json.dumps(data_payload).encode('utf-8'), headers=headers)
        
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                all_posts.extend(data["results"])
                has_more = data["has_more"]
                next_cursor = data["next_cursor"]
                print(f"Fetched {len(all_posts)} posts so far...")
        except urllib.error.HTTPError as e:
            print(f"Error fetching data: {e}")
            return []
            
    return all_posts

def archive_page(page_id):
    url = f"{PAGE_URL_BASE}/{page_id}"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    data = json.dumps({"archived": True}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method="PATCH")
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.getcode() == 200:
                return True
    except Exception as e:
        print(f"Failed to archive {page_id}: {e}")
    return False

def main():
    if not NOTION_TOKEN:
        print("Error: NOTION_TOKEN not set.")
        return

    posts = get_all_posts()
    if not posts:
        print("No posts found or error fetching.")
        return

    # Group by Title
    posts_by_title = defaultdict(list)
    for post in posts:
        try:
            props = post.get("properties", {})
            title_objs = props.get("Content ", {}).get("title", [])
            if title_objs:
                title = title_objs[0].get("plain_text", "")
                posts_by_title[title].append(post)
        except:
            continue

    total_deleted = 0
    
    print("\nAnalyzing duplicates...")
    for title, items in posts_by_title.items():
        if len(items) > 1:
            print(f"Found {len(items)} copies of: '{title}'")
            
            # Sort by creation time (keep oldest)
            # Notion dates are ISO 8601 strings
            items.sort(key=lambda x: x["created_time"])
            
            # Keep the first one (oldest), delete the rest
            to_keep = items[0]
            to_delete = items[1:]
            
            print(f"   -> Keeping version from {to_keep['created_time']}")
            
            for item in to_delete:
                print(f"   -> Deleting version from {item['created_time']} ({item['id']})...")
                if archive_page(item['id']):
                    print("      [Deleted]")
                    total_deleted += 1
                else:
                    print("      [Error Deleting]")
                time.sleep(0.2) # Rate limit friendly

    print("\n------------------------------------------------")
    if total_deleted > 0:
        print(f"✅ Cleanup complete. Removed {total_deleted} duplicate entries.")
    else:
        print("✅ No duplicates needed deleting.")
    print("------------------------------------------------")

if __name__ == "__main__":
    main()
