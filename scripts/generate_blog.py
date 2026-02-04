import csv
import os
import re

# Configuration
CSV_FILE = 'webflow_blog_import.csv'
TEMPLATE_FILE = 'blog-post-template.html'
OUTPUT_DIR = 'blog'
RECURSOS_HTML = 'recursos.html'

def slugify(text):
    text = text.lower()
    return re.sub(r'[^a-z0-9]+', '-', text).strip('-')

def clean_content(html_content):
    # Basic cleanup
    # Remove 'n' before tags like n<p>, n<h1>, n<h4>
    content = html_content.replace('n<', '<')
    # Remove escaped newlines if any
    content = content.replace('\\n', '')
    return content

def generate_blog():
    # Ensure output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Read Template
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        template = f.read()

    posts = []

    # Read CSV
    # Headers: post_name,post_date,featured_image,post_content,slug
    # Read CSV
    # Structure appears to be: Title, Date, Image, Content, Slug
    with open(CSV_FILE, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if not row: continue
            if row[0] == 'Title': continue # Skip header
            
            # Safe get by index
            title = row[0] if len(row) > 0 else 'Sin Título'
            date_raw = row[1] if len(row) > 1 else ''
            date = date_raw.split(' ')[0] if date_raw else ''
            image = row[2] if len(row) > 2 else ''
            content = clean_content(row[3]) if len(row) > 3 else ''
            slug = row[4] if len(row) > 4 else ''
            
            if not slug:
                slug = slugify(title)
            
            # Generate individual HTML file
            filename = f"{slug}.html"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            # Simple Category Logic (Mock)
            category = "Recursos"
            
            html_content = template.replace('{TITLE}', title)
            html_content = html_content.replace('{DATE}', date)
            html_content = html_content.replace('{CATEGORY}', category)
            html_content = html_content.replace('{CONTENT}', content)
            html_content = html_content.replace('{IMAGE}', image)
            html_content = html_content.replace('{EXCERPT}', title) # Use title as meta desc for now

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"Generated: {filepath}")
            
            # Add to list for index
            posts.append({
                'title': title,
                'slug': slug,
                'date': date,
                'image': image,
                'category': category
            })

    # Update Recursos.html
    update_recursos_index(posts)

def update_recursos_index(posts):
    with open(RECURSOS_HTML, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generate Grid Items
    grid_html = ""
    for post in posts:
        # Check if local image exists, else use placeholder
        img_src = post['image'] if post['image'] else 'assets/images/branding/logos/Core Competent.png'
        
        card = f"""
        <!-- Article Card -->
        <div class="animate-up" style="display: flex; flex-direction: column;">
            <div style="height: 200px; overflow: hidden; border-radius: 4px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 1rem;">
                <a href="blog/{post['slug']}.html">
                    <img src="{img_src}" alt="{post['title']}" 
                         onerror="this.src='assets/images/branding/logos/Core Competent.png'"
                         style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s;">
                </a>
            </div>
            <div class="glass-panel-light" style="padding: 1.5rem; flex-grow: 1; display: flex; flex-direction: column;">
                <span style="font-size: 0.7rem; color: var(--color-accent); font-weight: 700; uppercase; margin-bottom:0.5rem;">{post['date']}</span>
                <h3 style="font-size: 1.1rem; margin: 0 0 1rem; line-height: 1.3;">
                    <a href="blog/{post['slug']}.html" style="color: white; text-decoration: none;">{post['title']}</a>
                </h3>
                <a href="blog/{post['slug']}.html" style="font-size: 0.8rem; font-weight: 700; color: #D9A975; text-decoration: none; margin-top: auto;">Leer más &rarr;</a>
            </div>
        </div>
        """
        grid_html += card

    # Inject into resources.html
    # We look for the grid container. 
    # For safety, I'll recommend the user to add "<!-- BLOG_LIST_START -->" in the next step, 
    # but for now, I will replace the existing content of the specific grid div if I can find a marker.
    # Actually, simplest is to look for the known grid layout in resources.html or use an anchor.
    
    start_marker = "<!-- BLOG_LIST_START -->"
    end_marker = "<!-- BLOG_LIST_END -->"
    
    if start_marker in content and end_marker in content:
        pattern = re.compile(f'{re.escape(start_marker)}.*?{re.escape(end_marker)}', re.DOTALL)
        new_content = pattern.sub(f"{start_marker}\n<div class='grid grid-3' style='gap: 2rem;'>{grid_html}</div>\n{end_marker}", content)
        
        with open(RECURSOS_HTML, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Updated recursos.html with blog grid.")
    else:
        print("Warning: Could not find <!-- BLOG_LIST_START --> markers in recursos.html")

if __name__ == '__main__':
    generate_blog()
