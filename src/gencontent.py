import os
from pathlib import Path
from block_markdown import markdown_to_html_node
from htmlnode import ParentNode

def extract_title(markdown: str) -> str:
    if not markdown.startswith("# "):
        raise Exception("No h1 header found")
    return markdown.split("# ", maxsplit=1)[1]


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
# read() needs a file object, so we need to turn the path string into file objects
    with open(from_path, mode='r') as f:
        markdown_from_path = f.read()
    with open(template_path, mode='r') as f:
        template_text = f.read()
    md_node = markdown_to_html_node(markdown_from_path)
    page_content = md_node.to_html()
    page_title = extract_title(markdown_from_path)
    # replace the title, then replace the content, reassigning variables because replace() doesn't modify things in place
    template_text = template_text.replace("{{ Title }}", page_title)
    template_text = template_text.replace("{{ Content }}", page_content)
    template_text = template_text.replace('href="/', 'href="' + basepath)
    template_text = template_text.replace('src="/', 'src="' + basepath)
    # Write the new full HTML page to a file at dest_path. Be sure to create any necessary directories if they don't exist.
    # make dirs, open, write
    dest_path_dirname = os.path.dirname(dest_path)
    if dest_path_dirname != "":
        os.makedirs(dest_path_dirname, exist_ok=True)
    with open(dest_path, mode='w') as f:
        f.write(template_text)


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str) -> None:
    content_files = os.listdir(dir_path_content)
    for file in content_files:
        content_file_path = os.path.join(dir_path_content, file)
        dest_file_path = os.path.join(dest_dir_path, file)
        if not os.path.isfile(content_file_path):
            generate_pages_recursive(content_file_path, template_path, dest_file_path, basepath)
        else:
            if file.endswith(".md"):
                # string methods work but let's learn how to use more robust tools
                p = Path(dest_file_path)
                html_path = p.with_suffix(".html")
                str_html_path = str(html_path)
                generate_page(content_file_path, template_path, str_html_path, basepath)
