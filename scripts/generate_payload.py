
import csv
import json
import re
from html.parser import HTMLParser
from datetime import datetime

CSV_FILE = "webflow_blog_import.csv"
OUTPUT_FILE = "scripts/notion_import_payload.json"

# --- HTML Parser for Notion ---

class NotionHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.blocks = []
        self.current_block = None
        self.current_text = []
        self.list_stack = [] # 'bulleted_list_item' or 'numbered_list_item'
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        if tag in ['h1', 'h2', 'h3']:
            self.flush_text()
            level = int(tag[1])
            self.current_block = {
                "object": "block",
                "type": f"heading_{level}",
                f"heading_{level}": {"rich_text": [], "color": "default"}
            }
            
        elif tag == 'p':
            self.flush_text()
            self.current_block = {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [], "color": "default"}
            }
            
        elif tag == 'ul':
            self.list_stack.append('bulleted_list_item')
            
        elif tag == 'ol':
            self.list_stack.append('numbered_list_item')
            
        elif tag == 'li':
            self.flush_text()
            list_type = self.list_stack[-1] if self.list_stack else 'bulleted_list_item'
            self.current_block = {
                "object": "block",
                "type": list_type,
                list_type: {"rich_text": [], "color": "default"}
            }
            
        elif tag == 'blockquote':
            self.flush_text()
            self.current_block = {
                "object": "block",
                "type": "quote",
                "quote": {"rich_text": [], "color": "default"}
            }

        elif tag == 'img':
            self.flush_text()
            src = attrs_dict.get('src')
            if src:
                # Basic fix for relative paths if needed, or just use as is
                # Assuming src is a valid URL or path Notion can handle (Notion needs hosted URLs usually)
                # But for now we just create the block. 
                # Note: Notion API requires external URLs to be accessible. 
                # If these are local assets, they won't render. 
                # We'll map them as external images for now.
                self.blocks.append({
                    "object": "block",
                    "type": "image",
                    "image": {
                        "type": "external",
                        "external": {"url": src} 
                    }
                })

    def handle_endtag(self, tag):
        if tag in ['h1', 'h2', 'h3', 'p', 'li', 'blockquote']:
            self.flush_text()
        elif tag in ['ul', 'ol']:
            if self.list_stack:
                self.list_stack.pop()

    def handle_data(self, data):
        data = data.strip()
        if not data:
            return
            
        if self.current_block:
            # Append to valid block
            block_type = self.current_block['type']
            if block_type in ['heading_1', 'heading_2', 'heading_3', 'paragraph', 'bulleted_list_item', 'numbered_list_item', 'quote']:
                 self.current_block[block_type]['rich_text'].append({
                     "type": "text",
                     "text": {"content": data + " "} # Add space for safety between chunks
                 })

    def flush_text(self):
        if self.current_block:
            # Only add block if it has text or is an image (images are added directly)
            # Check content for text blocks
            block_type = self.current_block['type']
            if block_type != 'image':
                content = self.current_block[block_type]['rich_text']
                if content:
                    self.blocks.append(self.current_block)
            self.current_block = None

    def parse_html(self, html_content):
        # Reset
        self.blocks = []
        self.current_block = None
        self.list_stack = []
        
        # Feed
        self.feed(html_content)
        self.flush_text()
        
        # Limit to 100 blocks per request (Notion API limit for children)
        # If more, we truncate for Safety in this MVP import
        return self.blocks[:95] 


def main():
    payloads = []
    
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row.get('Title', 'Untitled')
            date_str = row.get('Date', '')
            content_html = row.get('Content', '')
            
            # Format Date for Notion (ISO 8601 YYYY-MM-DD)
            try:
                dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                iso_date = dt.strftime('%Y-%m-%d')
            except ValueError:
                iso_date = datetime.now().strftime('%Y-%m-%d') # Fallback
                
            # Parse Content
            parser = NotionHTMLParser()
            children_blocks = parser.parse_html(content_html)
            
            # Construct Notion Entry
            entry = {
                "properties": {
                    "Content ": { # Title property name in DB
                        "title": [
                            {"text": {"content": title}}
                        ]
                    },
                    "Publish Date": {
                        "date": {"start": iso_date}
                    },
                    "Status": {
                        "status": {"name": "Published"}
                    },
                    "Type": {
                        "select": {"name": "Blog"}
                    },
                    "Platform": {
                         "select": {"name": "Blog"}
                    }
                },
                "children": children_blocks
            }
            payloads.append(entry)
            
    # Save to JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(payloads, f, indent=2)
        
    print(f"Generated payload for {len(payloads)} posts at {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
