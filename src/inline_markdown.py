import re
from textnode import TextType, TextNode

# Extractors

def extract_markdown_images(text:str) -> list[tuple[str, str]]:
    alt_text_url = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return alt_text_url

def extract_markdown_links(text:str) -> list[tuple[str, str]]:
    alt_text_url = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return alt_text_url

# Splitters

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            sections = old_node.text.split(delimiter)
            if len(sections) % 2 == 0:
                raise Exception("missing closing delimiter")
            for index, section in enumerate(sections):
                if section == "":
                    continue
                if index % 2 == 0:
                    new_nodes.append(TextNode(section, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(section, text_type))
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    # The extractors automatically return an empty list if no matches are found, so they can be used as a check.
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            # a .TEXT type can't be split further, so it goes on to the list as is.
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        original_text = node.text

        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            # 1st iteration returns section[0] and section[1], where section[0] is the text before the image and section[1] is the
            # image part
            original_text = sections[1]
            # 2nd iteration will pick up from section[1].
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
        # Once the image loop finishes, whatever is left in original_text will be text, since our extractor filters out links only.
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    # The extractors automatically return an empty list if no matches are found, so they can be used as a check.
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            # a .TEXT type can't be split further, so it goes on to the list as is.
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        original_text = node.text

        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            # 1st iteration returns section[0] and section[1], where section[0] is the text before the link and section[1] is the
            # image part
            original_text = sections[1]
            # 2nd iteration will pick up from section[1].
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
        # Once the image loop finishes, whatever is left in original_text will be text, since our extractor filters out links only.
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

# Text to TextNodes

def text_to_textnodes(text:str) -> list[TextNode]:
    # Preparing the text for SND
    nodes = [TextNode(text, TextType.TEXT)]
    # Now SND can take it:

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes
