from enum import Enum
from sys import maxsize
from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'


def markdown_to_blocks(markdown:str) -> list[str]:
    split_blocks = markdown.split("\n\n")
    stripped_blocks = []
    for block in split_blocks:
        stripped_blocks.append(block.strip())
    clean_blocks = []
    for block in stripped_blocks:
        if block:
            clean_blocks.append(block)
    return clean_blocks


def block_to_block_type(block:str) -> BlockType:
    if block.startswith(
        (
            "# ",
            "## ",
            "### ",
            "#### "
            "##### ",
            "###### ",
        )
    ):
        return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    quote_lines = block.split("\n")
    results = [line.startswith(">") for line in quote_lines]
    if all(results):
        return BlockType.QUOTE

    unordered_list_items = block.split("\n")
    results = [item.startswith("- ") for item in unordered_list_items]
    if all(results):
        return BlockType.UNORDERED_LIST

    ordered_list_items = block.split("\n")
    prefix = 1
    for item in ordered_list_items:
        if not item.startswith(f"{prefix}"):
            return BlockType.PARAGRAPH
        if item.startswith(f"{prefix}. "):
            prefix += 1
    return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def _text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes

# Type helper function structure:
# get rid of the markdown markers
# call _text_to_children on the cleaned up text to get the inline children
# attach the little LeafNodes to a ParentNode with the corresponding HTML tag
# return the parent node

def _paragraph_to_html_node(paragraph: str) -> ParentNode:
    clean_paragraph = paragraph.replace("\n", " ")
    paragraph_leaf_nodes = _text_to_children(clean_paragraph)
    paragraph_branch_node = ParentNode("p", paragraph_leaf_nodes, None)
    return paragraph_branch_node

def _heading_to_html_node(heading: str) -> ParentNode:
    # need to remove the #s from the head, count them and return their count
    # then use that count to build the tag
    split_heading = heading.split(" ", maxsplit=1)
    number = len(split_heading[0])
    clean_heading = split_heading[1]
    tag = f"h{number}"
    heading_leaf_nodes = _text_to_children(clean_heading)
    heading_branch_node = ParentNode(tag, heading_leaf_nodes, None)
    return heading_branch_node


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
