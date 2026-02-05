
import os
import json
import urllib.request
import urllib.error
from collections import Counter

# Configuration
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID", "2fd0385f-9445-81cc-8703-f8174967321b")
API_URL = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

def check_duplicates():
    if not NOTION_TOKEN:
        print("Error: NOTION_TOKEN env var not set.")
        print("Please export it: export NOTION_TOKEN=your_token")
        return

    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    all_titles = []
    has_more = True
    next_cursor = None
    page_count = 0

    print(f"Checking for duplicates in database {DATABASE_ID}...")

    while has_more:
        data_payload = {"page_size": 100}
        if next_cursor:
            data_payload["start_cursor"] = next_cursor

        req = urllib.request.Request(API_URL, data=json.dumps(data_payload).encode('utf-8'), headers=headers)

        try:
            with urllib.request.urlopen(req) as response:
                response_data = json.loads(response.read().decode('utf-8'))
                
                results = response_data.get("results", [])
                
                for page in results:
                    page_count += 1
                    try:
                        props = page.get("properties", {})
                        # Adjust property name if needed. Based on import script it's "Content "
                        title_objs = props.get("Content ", {}).get("title", [])
                        if title_objs:
                            title_text = title_objs[0].get("plain_text", "")
                            all_titles.append(title_text)
                        # else:
                        #     all_titles.append("[No Title]")
                    except Exception as e:
                        pass 

                has_more = response_data.get("has_more", False)
                next_cursor = response_data.get("next_cursor")
                print(f"Fetched {page_count} items...")
                
        except urllib.error.HTTPError as e:
            print(f"HTTP Error: {e.code} - {e.reason}")
            print(e.read().decode('utf-8'))
            return
        except Exception as e:
            print(f"Error: {str(e)}")
            return

    print(f"\nTotal items: {len(all_titles)}")
    
    counts = Counter(all_titles)
    duplicates = {k: v for k, v in counts.items() if v > 1}

    if duplicates:
        print(f"\n⚠️ FOUND {len(duplicates)} DUPLICATE TITLES:")
        print("----------------------------------------")
        for title, count in duplicates.items():
            print(f"x{count} - {title}")
        print("----------------------------------------")
    else:
        print("\n✅ NO DUPLICATES FOUND. All titles are unique.")

if __name__ == "__main__":
    check_duplicates()
