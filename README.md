# Roam Research Page Markdown Extractor With Linked References

Roam Research is a powerful tool for networked thought, but its current export options have limitations. When exporting a single page to Markdown, Roam doesn't include the linked references (backlinks) in the export. This script fills that gap by extracting the full content of a specified page to Markdown, including all linked references. This makes Roam exports more useful for AI tools such as Claude Projects.

## Requirements

- Python 3.6 or higher

## How to Use

1. Export your entire Roam Research graph as JSON (go to All Pages > Export All > JSON)
2. Run this script, specifying the JSON file, the title of the page you want to extract, and the desired output file name

```python extract_roam_markdown.py <json_export.json> <page_title> <output_file.md>```

3. The resulting Markdown file will contain the page content and all its linked references

## Output

The script generates a Markdown file with the following structure:

1. Page title
2. Page content
3. Linked References section
   - Sorted by date (if applicable)
   - Each reference includes the referencing block and its sub-blocks


## License

This project is open-source and available under the MIT License.