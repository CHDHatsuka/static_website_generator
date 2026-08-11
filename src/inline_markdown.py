import re
from textnode import TextNode

def extract_markdown_images(text:str) -> list[tuple[str, str]]:
    alt_text_url = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return alt_text_url

def extract_markdown_links(text:str) -> list[tuple[str, str]]:
    alt_text_url = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return alt_text_url

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    # The extractors automatically return an empty list if no matches are found, so they can be used as a check.
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            # a .TEXT type can't be split further, so it goes on to the list as is.
            new_nodes.append(node)
    return new_nodes

    for node in old_nodes:
        images = extract_markdown_images(node.text)
        original_text = node.text
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            # 1st iteration return section[0] and section[1]
            original_text = sections[1]
            # 2nd iteration will pick up from section[1]
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
