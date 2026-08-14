import unittest
from block_markdown import BlockType, markdown_to_blocks, block_to_block_type

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
# TIL multiline string syntax and that they should not be indented because tabs are interpreted as \n
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty_markdown(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_many_newlines(self):
        md = """











        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_block_to_block_type_paragraph(self):
        block8 = "This is just a paragraph."
        self.assertEqual(block_to_block_type(block8), BlockType.PARAGRAPH)

    def test_block_to_block_type_heading(self):
        block1 = "# one heading"
        self.assertEqual(block_to_block_type(block1), BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block2 = """```
        code```"""
        self.assertEqual(block_to_block_type(block2), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block5 = ">This is\n>supposed to be\n>a haiku."
        self.assertEqual(block_to_block_type(block5), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        block6 = "- Lettuce\n- Bananas\n- Milk"
        self.assertEqual(block_to_block_type(block6), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        block7 = "1. First you do this\n2. Then you do that\n3. Then you call me\n4. Finally, it's done"
        self.assertEqual(block_to_block_type(block7), BlockType.ORDERED_LIST)

if __name__ == "__main__":
    unittest.main()
