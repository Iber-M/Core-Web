import re
import os
import html
import csv

# Configuration
BACKUP_SQL_PATH = "/Users/iberm/Library/CloudStorage/OneDrive-CoreCompetent/03 Sales & Mkt/🎨 Marketing y Brand/02 Pagina Web y SEO/05 Archivo/Core web legacy Backup/backup.sql"
OUTPUT_CSV = "webflow_export.csv"
TABLE_PREFIX = "wp_5vd2r31yao_"

def parse_insert_values(full_text, table_name):
    """
    Finds ALL INSERT statements for a specific table and parses values.
    """
    start_pattern = f"INSERT INTO `{table_name}` VALUES ("
    rows = []
    
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
                if char == 'n': current_value += '\n'
                elif char == 'r': current_value += '\r'
                elif char == 't': current_value += '\t'
                elif char == '\\': current_value += '\\'
                elif char == "'": current_value += "'"
                elif char == '"': current_value += '"'
                else: current_value += char # unknown escape, keep it
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
                while cursor < length:
                    next_char = full_text[cursor]
                    if next_char == ',':
                        cursor += 1
                        while cursor < length and full_text[cursor] in [' ', '\n', '\r', '\t']:
                            cursor += 1
                        if cursor < length and full_text[cursor] == '(':
                            cursor += 1
                            break 
                        continue
                    if next_char == ';':
                        return local_rows, cursor
                    if next_char in [' ', '\n', '\r', '\t']:
                        cursor += 1
                        continue
                    if next_char == '(':
                        cursor += 1
                        break
                    cursor += 1
                continue
            current_value += char
            cursor += 1
        return local_rows, cursor

    current_search_idx = 0
    while True:
        idx = full_text.find(start_pattern, current_search_idx)
        if idx == -1:
            break
        new_rows, end_idx = parse_one_statement(idx)
        rows.extend(new_rows)
        current_search_idx = end_idx
        
    return rows

def clean_divi_content(content):
    """
    Strips Divi shortcodes while preserving text content.
    """
    # 1. Strip all et_pb shortcodes
    content = re.sub(r'\[\/?et_pb_.*?\]', '', content)
    
    # 2. Handle remaining common WP shortcodes
    content = re.sub(r'\[\/?caption.*?\]', '', content)
    
    # 3. Unescape HTML
    content = html.unescape(content)
    
    # 4. Clean up whitespace
    content = content.strip()
    
    return content

def main():
    print(f"Reading {BACKUP_SQL_PATH} into memory...")
    with open(BACKUP_SQL_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        full_text = f.read()

    print("Parsing Tables...")
    posts_raw = parse_insert_values(full_text, f"{TABLE_PREFIX}posts")
    meta_raw = parse_insert_values(full_text, f"{TABLE_PREFIX}postmeta")
    terms_raw = parse_insert_values(full_text, f"{TABLE_PREFIX}terms")
    taxonomy_raw = parse_insert_values(full_text, f"{TABLE_PREFIX}term_taxonomy")
    rels_raw = parse_insert_values(full_text, f"{TABLE_PREFIX}term_relationships")

    print(f"Stats: Posts({len(posts_raw)}), Meta({len(meta_raw)}), Terms({len(terms_raw)}), Tax({len(taxonomy_raw)}), Rels({len(rels_raw)})")

    # Mapping logic
    post_id_to_meta = {} # post_id -> {key: val}
    for m in meta_raw:
        if len(m) < 4: continue
        pid, key, val = m[1], m[2], m[3]
        if pid not in post_id_to_meta: post_id_to_meta[pid] = {}
        post_id_to_meta[pid][key] = val

    term_id_to_name = {t[0]: t[1] for t in terms_raw if len(t) > 1}
    tax_id_to_term_id = {tx[0]: tx[1] for tx in taxonomy_raw if len(tx) > 2 and tx[2] == 'category'}
    
    post_id_to_terms = {} # post_id -> [term_names]
    for r in rels_raw:
        if len(r) < 2: continue
        pid, tax_id = r[0], r[1]
        if tax_id in tax_id_to_term_id:
            term_id = tax_id_to_term_id[tax_id]
            if term_id in term_id_to_name:
                name = term_id_to_name[term_id]
                if pid not in post_id_to_terms: post_id_to_terms[pid] = []
                post_id_to_terms[pid].append(name)

    # Main export loop
    webflow_data = []
    
    # Headers for Webflow
    headers = ["Item Name", "Slug", "Published Date", "Post Body", "Featured Image", "Categories"]

    for p in posts_raw:
        # Schema: 0:ID, 2:date, 4:content, 5:title, 7:status, 11:name(slug), 20:type
        if len(p) < 21: continue
        pid = p[0]
        p_type = p[20]
        p_status = p[7]
        
        if p_type in ['post', 'page'] and p_status == 'publish':
            title = p[5]
            slug = p[11]
            date = p[2]
            content = clean_divi_content(p[4])
            
            # Resolve Image
            featured_image = ""
            meta = post_id_to_meta.get(pid, {})
            thumb_id = meta.get('_thumbnail_id')
            if thumb_id and thumb_id != '0':
                # thumb_id is a post_id of type 'attachment'
                # find it in postmeta
                attachment_meta = post_id_to_meta.get(thumb_id, {})
                file_path = attachment_meta.get('_wp_attached_file')
                if file_path:
                    # Construct a URL or keep path. Webflow needs a URL usually if importing from web, 
                    # but if providing a local path, user might need to upload manually or we use placeholder.
                    # Let's provide the relative path in the backup.
                    featured_image = file_path
            
            # Resolve Categories
            categories = ", ".join(post_id_to_terms.get(pid, []))
            
            webflow_data.append([title, slug, date, content, featured_image, categories])

    print(f"Exporting {len(webflow_data)} items to {OUTPUT_CSV}...")
    with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(webflow_data)

    print("Success! File generated.")

if __name__ == "__main__":
    main()
