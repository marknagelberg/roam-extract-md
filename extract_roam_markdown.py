import json
from datetime import datetime
import re
import sys
import argparse

def load_roam_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def find_page(data, title):
    return next((page for page in data if page.get('title') == title), None)

def extract_content(page, level=0):
    content = []
    if 'string' in page:
        content.append('  ' * level + page['string'])
    if 'children' in page:
        for child in page['children']:
            content.extend(extract_content(child, level + 1))
    return content

def extract_referencing_blocks(page, title, level=0):
    blocks = []
    if 'string' in page and f'[[{title}]]' in page['string']:
        blocks.append(('  ' * level + page['string'], []))
        if 'children' in page:
            for child in page['children']:
                blocks[-1][1].extend(extract_content(child, level + 1))
    elif 'children' in page:
        for child in page['children']:
            blocks.extend(extract_referencing_blocks(child, title, level + 1))
    return blocks

def find_references(data, title):
    references = []
    for page in data:
        if page.get('title') != title:  # Exclude the main page itself
            ref_blocks = extract_referencing_blocks(page, title)
            if ref_blocks:
                references.append((page.get('title', 'Untitled'), ref_blocks))
    return references

def is_date(string):
    date_pattern = r'^(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(st|nd|rd|th),\s+\d{4}$'
    return bool(re.match(date_pattern, string))

def parse_date(date_string):
    try:
        # Remove ordinal indicators
        date_string = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_string)
        return datetime.strptime(date_string, "%B %d, %Y")
    except ValueError:
        return datetime.min

def sort_references(references):
    return sorted(references, key=lambda x: (not is_date(x[0]), parse_date(x[0]) if is_date(x[0]) else datetime.min), reverse=True)

def generate_markdown(title, content, references):
    markdown = f"# {title}\n\n"
    markdown += "\n".join(content)
    markdown += "\n\n## Linked References\n\n"
    for ref_title, ref_blocks in references:
        markdown += f"### {ref_title}\n\n"
        for block, sub_blocks in ref_blocks:
            markdown += block + "\n"
            if sub_blocks:
                markdown += "\n".join(sub_blocks) + "\n"
            markdown += "\n"
    return markdown

def main():
    parser = argparse.ArgumentParser(description='Extract and format Roam Research page content with linked references.')
    parser.add_argument('json_file', help='Path to the Roam Research JSON export file')
    parser.add_argument('page_title', help='Title of the page to extract')
    parser.add_argument('output_file', help='Path to the output Markdown file')
    
    args = parser.parse_args()
    
    data = load_roam_data(args.json_file)
    page = find_page(data, args.page_title)
    
    if not page:
        print(f"Page '{args.page_title}' not found.")
        return
    
    content = extract_content(page)
    references = find_references(data, args.page_title)
    sorted_references = sort_references(references)
    markdown = generate_markdown(args.page_title, content, sorted_references)
    
    with open(args.output_file, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    print(f"Markdown file generated: {args.output_file}")

if __name__ == "__main__":
    main()