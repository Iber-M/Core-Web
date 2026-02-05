
import os
import json
import urllib.request
import urllib.error
import glob

# Configuration
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
# We will search for the DB ID dynamically or user can set it
DATABASE_NAME = "Recursos Descargables"
API_URL_SEARCH = "https://api.notion.com/v1/search"
API_URL_PAGES = "https://api.notion.com/v1/pages"

def find_database_id():
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    payload = {
        "query": DATABASE_NAME,
        "filter": {"value": "database", "property": "object"}
    }
    
    try:
        req = urllib.request.Request(API_URL_SEARCH, data=json.dumps(payload).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            results = data.get("results", [])
            if results:
                return results[0]["id"]
    except Exception as e:
        print(f"Error searching for database: {e}")
    return None

def create_resource_entry(db_id, filename):
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # Clean filename for title
    title = os.path.splitext(os.path.basename(filename))[0].replace("_", " ")
    
    payload = {
        "parent": {"database_id": db_id},
        "properties": {
            "Nombre": {
                "title": [{"text": {"content": title}}]
            },
            "Tipo": {
                "select": {"name": "Guía"} # Default
            },
            "Estado": {
                "status": {"name": "Borrador"} # Default
            }
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text", 
                            "text": {"content": f"Archivo pendiente de subir: {filename}", "annotations": {"italic": True}}
                        }
                    ]
                }
            }
        ]
    }
    
    try:
        req = urllib.request.Request(API_URL_PAGES, data=json.dumps(payload).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req) as response:
            if response.getcode() == 200:
                print(f"✅ Created entry for: {title}")
                return True
    except urllib.error.HTTPError as e:
         print(f"❌ Failed to create {title}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    return False

def main():
    if not NOTION_TOKEN:
        print("Error: NOTION_TOKEN env var not set.")
        return

    print(f"Searching for database '{DATABASE_NAME}'...")
    db_id = find_database_id()
    
    if not db_id:
        print(f"❌ Could not find database named '{DATABASE_NAME}'. Please make sure you created it!")
        return
        
    print(f"Found Database ID: {db_id}")
    
    # Find PDFs
    pdf_files = glob.glob("assets/documents/*.pdf")
    if not pdf_files:
        print("No PDFs found in assets/documents/")
        return
        
    print(f"Found {len(pdf_files)} PDFs. Creating placeholders...")
    
    for pdf in pdf_files:
        create_resource_entry(db_id, pdf)
        
    print("\nDone! Please drag-and-drop the actual PDF files into the Notion rows.")

if __name__ == "__main__":
    main()
