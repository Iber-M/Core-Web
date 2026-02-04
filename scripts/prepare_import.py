
import csv
import json
import re
import sys
import os
from datetime import datetime
from html.parser import HTMLParser

# Configuration
CSV_FILE = 'webflow_blog_import.csv'
JSON_OUTPUT = 'scripts/notion_import_payload.json'

def truncate(text, limit=2000):
    return text[:limit]

def clean_text(text):
    if not text:
        return ""
    if text.startswith('n<'):
        text = text[1:]
    return text.strip()

class NotionBlockParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.blocks = []
        self.current_block = None
        self.current_tag_stack = []
        self.ignore_tags = ['div', 'span', 'body', 'html'] 
        
    def handle_starttag(self, tag, attrs):
        self.current_tag_stack.append(tag)
        
        if tag in self.ignore_tags:
            return

        block_type = None
        if tag in ['h1', 'h2']:
            block_type = 'heading_1'
        elif tag == 'h3':
            block_type = 'heading_2'
        elif tag in ['h4', 'h5', 'h6']:
            block_type = 'heading_3'
        elif tag == 'p':
            block_type = 'paragraph'
        elif tag == 'li':
            # Check parent to determine list type
            parent = self.current_tag_stack[-2] if len(self.current_tag_stack) > 1 else ''
            if parent == 'ol':
                block_type = 'numbered_list_item'
            else:
                block_type = 'bulleted_list_item'
        elif tag == 'blockquote':
            block_type = 'quote'
        elif tag == 'img':
            # Handle image immediately
            src = ''
            for k, v in attrs:
                if k == 'src':
                    src = v
            if src:
                self.blocks.append({
                    "object": "block",
                    "type": "callout",
                    "callout": {
                        "rich_text": [{"type": "text", "text": {"content": f"Image: {src}"}}],
                        "icon": {"emoji": "🖼️"}
                    }
                })
            return

        if block_type:
            # If we were already in a block (nested?), close it? 
            # Notion blocks aren't nested like HTML (except lists/details)
            # For simplicity, we treat tags as creating new blocks
            self.current_block = {
                "object": "block",
                "type": block_type,
                block_type: {
                    "rich_text": []
                }
            }
            self.blocks.append(self.current_block)

    def handle_endtag(self, tag):
        if self.current_tag_stack:
            self.current_tag_stack.pop()
        
        if tag not in self.ignore_tags and tag != 'img':
            self.current_block = None # Finished block

    def handle_data(self, data):
        text = data.strip()
        if not text:
            return
            
        # If we are not in a block (orphaned text), create a paragraph
        if self.current_block is None:
            # Only if text is substantial or we want to capture everything
            if self.current_tag_stack and self.current_tag_stack[-1] in self.ignore_tags:
                 # Text inside div/span -> make paragraph
                 self.current_block = {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": { "rich_text": [] }
                }
                 self.blocks.append(self.current_block)
            else:
                # Text at top level or unexpected, maybe add to previous block or make new
                pass

        if self.current_block:
            # Determine block type key
            btype = self.current_block['type']
            
            # Formatting annotations based on stack
            annotations = {}
            if 'b' in self.current_tag_stack or 'strong' in self.current_tag_stack:
                annotations['bold'] = True
            if 'i' in self.current_tag_stack or 'em' in self.current_tag_stack:
                annotations['italic'] = True
               
            self.current_block[btype]['rich_text'].append({
                "type": "text",
                "text": {"content": text},
                "annotations": annotations
            })

def make_payload():
    payloads = []
    
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = row.get('Title', 'Untitled')
                date_str = row.get('Date', '')
                slug = row.get('Slug', '')
                content = clean_text(row.get('Content', ''))
                image_path = row.get('Featured Image', '')
                
                iso_date = None
                if date_str:
                    try:
                        dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                        iso_date = dt.isoformat()
                    except ValueError:
                        iso_date = None

                # Category Detection Logic
                categories = []
                text_content = (title + " " + content).lower()
                
                keyword_map = {
                    "Reclutamiento": ["empleo", "vacante", "candidato", "selección", "entrevista", "cv", "curriculum", "reclutamiento", "contratación", "talento"],
                    "Liderazgo": ["líder", "liderazgo", "jefe", "management", "gestión", "equipo", "directivo"],
                    "Cultura": ["cultura", "clima", "valores", "ambiente", "bienestar", "organización"],
                    "Coaching": ["coaching", "coach", "desarrollo", "crecimiento", "capacitación", "soft skills"],
                    "Executive Search": ["ejecutivo", "headhunter", "ceo", "c-level", "alta dirección"],
                    "Estrategia": ["estrategia", "negocio", "planificación", "futuro", "tendencia", "mercado"]
                }
                
                for cat, keywords in keyword_map.items():
                    if any(k in text_content for k in keywords):
                        categories.append({"name": cat})
                        
                # Default category if none found
                if not categories:
                    categories.append({"name": "Estrategia"})

                properties = {
                    "Titulo": {
                        "title": [{"text": {"content": truncate(title)}}]
                    },
                    "Slug": {
                        "rich_text": [{"text": {"content": slug}}]
                    },
                    "Categoría": {
                        "multi_select": categories
                    }
                }
                
                if iso_date:
                    properties["Fecha de Publicación"] = {
                        "date": {"start": iso_date}
                    }
                
                # Parse content
                parser = NotionBlockParser()
                parser.feed(content)
                blocks = parser.blocks
                
                if image_path:
                     blocks.insert(0, {
                        "object": "block",
                        "type": "callout",
                        "callout": {
                            "rich_text": [{"type": "text", "text": {"content": f"Featured Image Path: {image_path}"}}],
                            "icon": {"emoji": "⭐"},
                            "color": "gray_background"
                        }
                    })

                payloads.append({
                    "properties": properties,
                    "children": blocks
                })
    except FileNotFoundError:
        print(f"Error: {CSV_FILE} not found.")
        return []
            
    return payloads

if __name__ == "__main__":
    payloads = make_payload()
    with open(JSON_OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(payloads, f, indent=2, ensure_ascii=False)
    print(f"Generated payload for {len(payloads)} posts.")
