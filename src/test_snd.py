import unittest
from platform import node
from textnode import TextType, TextNode
from split_nodes_delimiter import split_nodes_delimiter

class TestSND(unittest.TestCase):
    def test_text_type(self):
        old_nodes = [TextNode("**This text is already bold**", TextType.BOLD)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, old_nodes)

    def test_missing_delimiter(self):
        old_nodes = [TextNode("I forgot to close the *italic...", TextType.TEXT)]
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)

    def test_no_delimiter(self):
        old_nodes = [TextNode("I forgot to put italic", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
        self.assertEqual(new_nodes, old_nodes)

    def test_empty_old_nodes(self):
        old_nodes = []
        new_nodes = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
        self.assertEqual(new_nodes, old_nodes)

    def test_short_node(self):
        old_nodes = [TextNode("This is a **bold** short node", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        answer = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" short node", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, answer)

    def test_long_node(self):
        old_nodes = [TextNode("This is a **bold** longer node, **bold** again", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        answer = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" longer node, ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" again", TextType.TEXT)

        ]
        self.assertEqual(new_nodes, answer)

    def test_empty_string_head(self):
        old_nodes = [TextNode("**This node** starts bold", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        answer = [
            TextNode("This node", TextType.BOLD),
            TextNode(" starts bold", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, answer)

    def test_empty_string_tail(self):
        old_nodes = [TextNode("This node **ends bold**", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        answer = [
            TextNode("This node ", TextType.TEXT),
            TextNode("ends bold", TextType.BOLD)
        ]
        self.assertEqual(new_nodes, answer)


if __name__ == "__main__":
    unittest.main()
