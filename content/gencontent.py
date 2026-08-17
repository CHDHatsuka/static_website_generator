from block_markdown import markdown_to_html_node
from HTMLNode import ParentNode

def extract_title(markdown: str) -> str:
    if not markdown.startswith("# "):
        raise Exception("No h1 header found")
    return markdown.split("# ", maxsplit=1)[1]


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_from_path = from_path.read()
    template_text = template_path.read()
    md_node = markdown_to_html_node(markdown_from_path)
    page_content = ParentNode.to_html(md_node)
    page_title = extract_title(page_content)
    template_text.replace("{{ Title }}", page_title)
    template_text.replace("{{ Content }}", page_content)
    ####Write the new full HTML page to a file at dest_path. Be sure to create any necessary directories if they don't exist.
    ####make dirs, open, write
    dest_path_dirname = os.path.dirname(dest_path)
    if dest_path_dirname != "":
        os.makedirs(dest_path_dirname, exist_ok=True)
    with open(dest_path, mode='w') as f:
        f.write(template_text)
