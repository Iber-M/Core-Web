import re
import os
import html

# Configuration
BACKUP_SQL_PATH = "/Users/iberm/Library/CloudStorage/OneDrive-CoreCompetent/03 Sales & Mkt/🎨 Marketing y Brand/02 Pagina Web y SEO/05 Archivo/Core web legacy Backup/backup.sql"
OUTPUT_DIR = "restored_site"
ASSETS_DIR = "/Users/iberm/Library/CloudStorage/OneDrive-CoreCompetent/03 Sales & Mkt/🎨 Marketing y Brand/02 Pagina Web y SEO/05 Archivo/Core web legacy Backup/files"
TABLE_NAME = "wp_5vd2r31yao_posts"

def parse_insert_values(full_text):
    """
    Finds ALL INSERT statements for the posts table and parses values.
    Reads the whole text to handle newlines inside strings.
    """
    
    start_pattern = f"INSERT INTO `{TABLE_NAME}` VALUES ("
    
    rows = []
    
    # helper to parse one statement from a given start index
    def parse_one_statement(start_idx):
        cursor = start_idx + len(start_pattern)
        current_tuple = []
        current_value = ""
        in_quotes = False
        escape = False
        local_rows = []
        
        length = len(full_text)
        
        while cursor < length:
            char = full_text[cursor]
            
            if escape:
                current_value += char
                escape = False
                cursor += 1
                continue
                
            if char == '\\':
                escape = True
                cursor += 1
                continue
                
            if char == "'" and not escape:
                in_quotes = not in_quotes
                cursor += 1
                continue
                
            if char == ',' and not in_quotes:
                current_tuple.append(current_value)
                current_value = ""
                cursor += 1
                continue
                
            if char == ')' and not in_quotes:
                current_tuple.append(current_value)
                local_rows.append(current_tuple)
                current_tuple = []
                current_value = ""
                
                cursor += 1
                # Skip whitespace and find if next is ,( for more tuples or ; for end
                while cursor < length:
                    next_char = full_text[cursor]
                    if next_char == ',':
                        cursor += 1
                        # Check if next is (
                        while cursor < length and full_text[cursor] in [' ', '\n', '\r', '\t']:
                            cursor += 1
                        if cursor < length and full_text[cursor] == '(':
                            cursor += 1
                            break # Back to inner while loop for next tuple content
                        continue
                    if next_char == ';':
                        return local_rows, cursor # End of this INSERT statement
                    if next_char in [' ', '\n', '\r', '\t']:
                        cursor += 1
                        continue
                    # If we catch something else, it might be the start of next tuple without space
                    if next_char == '(':
                        cursor += 1
                        break
                    cursor += 1
                continue
                
            current_value += char
            cursor += 1
        return local_rows, cursor

    # Loop to find all INSERTs
    current_search_idx = 0
    while True:
        idx = full_text.find(start_pattern, current_search_idx)
        if idx == -1:
            break
        print(f"Found INSERT at index {idx}")
        new_rows, end_idx = parse_one_statement(idx)
        rows.extend(new_rows)
        current_search_idx = end_idx
        
    return rows

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        os.makedirs(os.path.join(OUTPUT_DIR, "posts"))

    # Symlink assets
    assets_target = os.path.join(OUTPUT_DIR, "assets")
    if not os.path.exists(assets_target):
        try:
            os.symlink(ASSETS_DIR, assets_target)
            print(f"Created symlink for assets: {assets_target} -> {ASSETS_DIR}")
        except Exception as e:
            print(f"Could not create symlink: {e}")

    print(f"Reading {BACKUP_SQL_PATH} into memory...")
    with open(BACKUP_SQL_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        full_text = f.read()
        
    print("Parsing SQL...")
    rows = parse_insert_values(full_text)
    print(f"Parsed {len(rows)} rows from posts table.")
    
    posts = []
    for val_list in rows:
        # Schema:
        # 0: ID
        # 4: post_content
        # 5: post_title
        # 7: post_status
        # 11: post_name (slug)
        # 20: post_type
        # 2: post_date
        
        if len(val_list) < 21: continue
        
        try:
            p_content = val_list[4]
            p_title = val_list[5]
            p_status = val_list[7]
            p_name = val_list[11]
            p_type = val_list[20]
            p_date = val_list[2]
            
            if p_type in ['post', 'page'] and p_status == 'publish':
                posts.append({
                    'title': p_title,
                    'content': p_content,
                    'slug': p_name,
                    'date': p_date,
                    'type': p_type
                })
        except IndexError:
            continue

    print(f"Found {len(posts)} published posts/pages.")

    # Generate Index
    index_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Core Web Legacy Archive</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 40px 20px; line-height: 1.6; color: #333; background: #f9f9f9; }
            .container { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
            h1 { color: #305c87; border-bottom: 2px solid #d1af77; padding-bottom: 15px; margin-top: 0; }
            .intro { color: #666; margin-bottom: 30px; }
            .post-list { display: grid; gap: 15px; }
            .post-item { padding: 15px; border-radius: 8px; border: 1px solid #eee; transition: all 0.2s; display: flex; align-items: center; text-decoration: none; color: inherit; }
            .post-item:hover { transform: translateX(5px); border-color: #d1af77; background: #fffdf9; }
            .date { color: #888; font-size: 0.85em; min-width: 130px; }
            .type { font-size: 0.7em; background: #305c87; color: white; padding: 2px 8px; border-radius: 20px; margin-right: 15px; text-transform: uppercase; font-weight: bold; letter-spacing: 0.5px; }
            .title { font-weight: 600; font-size: 1.1em; color: #333; }
            .count { margin-bottom: 20px; font-weight: bold; color: #d1af77; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Core Web Legacy Archive</h1>
            <p class="intro">Archivo histórico de contenidos restaurado el 2026-02-02.</p>
            <div class="count">Total de contenidos encontrados: {count}</div>
            <div class="post-list">
    """
    
    # Sort posts by date desc
    posts.sort(key=lambda x: x['date'], reverse=True)

    for post in posts:
        slug = post['slug'] if post['slug'] else f"id-{len(index_html)}"
        # Clean slug for filename
        slug = re.sub(r'[^a-zA-Z0-9-]', '-', slug)
        filename = f"posts/{slug}.html"
        
        index_html += f"""
        <a href="{filename}" class="post-item">
            <span class="type">{post['type']}</span>
            <span class="date">{post['date'].split(' ')[0]}</span>
            <span class="title">{post['title']}</span>
        </a>
        """
        
        # Generate Post HTML
        content = post['content']
        # Replace links to assets
        content = content.replace('https://www.corecompetent.mx/wp-content/', '../assets/wp-content/')
        content = content.replace('http://www.corecompetent.mx/wp-content/', '../assets/wp-content/')
        # Basic content cleanup (Divi shortcodes, etc is hard to clean perfectly but let's do newlines)
        content = content.replace('\\r\\n', '<br>').replace('\\n', '<br>')
        
        content = html.unescape(content)
        
        post_html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>{post['title']}</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 40px 20px; line-height: 1.8; color: #333; background: #fff; }}
                img {{ max-width: 100%; height: auto; border-radius: 8px; margin: 20px 0; }}
                a {{ color: #d1af77; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
                h1 {{ color: #305c87; line-height: 1.2; margin-top: 0; }}
                .meta {{ color: #888; margin-bottom: 30px; border-bottom: 1px solid #eee; padding-bottom: 15px; font-size: 0.9em; }}
                .nav {{ margin-bottom: 40px; }}
                .nav a {{ display: inline-block; padding: 8px 16px; background: #f0f0f0; border-radius: 6px; color: #555; }}
                .nav a:hover {{ background: #e0e0e0; text-decoration: none; }}
                .content {{ font-size: 1.1em; }}
                /* Basic Divi cleanup hiding */
                [class*="et_pb_"] {{ margin-bottom: 20px; }}
                blockquote {{ border-left: 5px solid #d1af77; padding: 10px 20px; background: #fdfaf3; font-style: italic; margin: 30px 0; }}
            </style>
        </head>
        <body>
            <div class="nav"><a href="../index.html">← Volver al Índice</a></div>
            <h1>{post['title']}</h1>
            <div class="meta">Publicado: {post['date']} | Tipo: {post['type']}</div>
            <div class="content">
                {content}
            </div>
        </body>
        </html>
        """
        
        with open(os.path.join(OUTPUT_DIR, filename), 'w', encoding='utf-8') as f:
            f.write(post_html)

    index_html = index_html.replace("{count}", str(len(posts)))
    index_html += """
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(os.path.join(OUTPUT_DIR, "index.html"), 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    print(f"Restoration complete. {len(posts)} items generated.")
    print(f"Open '{os.path.abspath(os.path.join(OUTPUT_DIR, 'index.html'))}' in your browser.")

if __name__ == "__main__":
    main()
