import os
import re
import csv
from html import unescape

def clean_divi_shortcodes(text):
    # Remove [et_pb_...][/et_pb_...] and single [et_pb_...] tags
    text = re.sub(r'\[/?et_pb.*?\]', '', text)
    # Remove leftover WordPress comments or markers
    text = re.sub(r'<!--.*?-->', '', text)
    # Clean multiple newlines
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()

def extract_meta(content):
    title = ""
    date = ""
    image = ""
    
    # Extract Title
    title_match = re.search(r'<h1>(.*?)</h1>', content)
    if title_match:
        title = title_match.group(1).strip()
    
    # Extract Date
    date_match = re.search(r'Publicado: (.*?) \|', content)
    if date_match:
        date = date_match.group(1).strip()
        
    # Extract Featured Image from Divi background attribute
    img_match = re.search(r'background_image="(.*?)"', content)
    if img_match:
        image = img_match.group(1).replace('../', '') # Cleanup relative path
    
    return title, date, image

def main():
    source_dir = "/Users/iberm/Mi unidad/Antigravity/Core-Web/data/restored_site/posts"
    output_file = "/Users/iberm/Mi unidad/Antigravity/Core-Web/webflow_blog_import.csv"
    
    posts = []
    
    for filename in os.listdir(source_dir):
        if filename.endswith(".html"):
            path = os.path.join(source_dir, filename)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                title, date, image = extract_meta(content)
                
                # Extract body
                body_match = re.search(r'<div class="content">(.*?)</div>', content, re.DOTALL)
                body = ""
                if body_match:
                    body = body_match.group(1)
                    body = clean_divi_shortcodes(body)
                
                posts.append({
                    'Title': unescape(title),
                    'Date': date,
                    'Featured Image': image,
                    'Content': body,
                    'Slug': filename.replace('.html', '')
                })
                
    # Save to CSV
    keys = posts[0].keys()
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(posts)
        
    print(f"Successfully processed {len(posts)} posts into {output_file}")

if __name__ == "__main__":
    main()
