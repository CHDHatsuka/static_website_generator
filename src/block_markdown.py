from enum import Enum

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
