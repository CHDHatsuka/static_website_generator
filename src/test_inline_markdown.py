from pydoc import text
import unittest
from textnode import TextType, TextNode
from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)

class TestInlineMarkdown(unittest.TestCase):
# Extractor test suite
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is a link to [Reddit](https://www.reddit.com)!"
        )
        self.assertListEqual(
            [
                ("Reddit","https://www.reddit.com")
            ],
            matches
        )

    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
            "This text has ![img1](https://i.imgur.com/zjjcJKZ.png) and ![img2](https://i.imgur.com/zjjc000.png)"
        )
        self.assertListEqual(
            [("img1", "https://i.imgur.com/zjjcJKZ.png"),
            ("img2", "https://i.imgur.com/zjjc000.png"),
            ],
            matches
        )

    def test_extract_multiple_links(self):
        matches = extract_markdown_links(
            "This text has [link1](https://www.reddit.com) and [link2](https://www.reddit.com)!"
        )
        self.assertListEqual(
            [
                ("link1", "https://www.reddit.com"),
                ("link2", "https://www.reddit.com"),
            ],
            matches
        )

    def test_extract_only_img(self):
        matches = extract_markdown_images(
            "This text has ![an img](https://i.imgur.com/zjjcJKZ.png) and [a link](https://www.reddit.com)"
        )
        self.assertListEqual(
            [
                ("an img", "https://i.imgur.com/zjjcJKZ.png"),
            ],
            matches
        )

    def test_extract_only_text(self):
        matches = extract_markdown_links(
            "This text has ![an img](https://i.imgur.com/zjjcJKZ.png) and [a link](https://www.reddit.com)"
        )
        self.assertListEqual(
            [
                ("a link", "https://www.reddit.com"),
            ],
            matches
        )

    def test_empty_img_alt(self):
        matches = extract_markdown_images(
            "I forgot to add alt text ![](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [
                ("", "https://i.imgur.com/zjjcJKZ.png"),
            ],
            matches
        )

    def test_empty_img_url(self):
        matches = extract_markdown_images(
            "I forgot to add url ![oh no]()"
        )
        self.assertListEqual(
            [
                ("oh no", ""),
            ],
            matches
        )

    def test_empty_link_text(self):
        matches = extract_markdown_links(
            "I forgot to add text [](https://www.reddit.com)"
        )
        self.assertListEqual(
            [
                ("", "https://www.reddit.com"),
            ],
            matches
        )

    def test_empty_link_url(self):
        matches = extract_markdown_links(
            "I forgot to add url [oh no]()"
        )
        self.assertListEqual(
            [
                ("oh no", ""),
            ],
            matches
        )

# Node splitter suite

    def test_text_type(self):
        old_nodes = [TextNode("**This text is already bold**", TextType.BOLD)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, old_nodes)

    def test_missing_delimiter(self):
        old_nodes = [TextNode("I forgot to close the _italic...", TextType.TEXT)]
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)

# Theoretically, the censored word could still be parsed as an empty bold markdown
# and be turned into an empty bold node.
# However, because of how split_nodes_delimiter looks for closing delimiters
# (by checking len(old_node.text.split(delimiter)) % 2 == 0)),
# it never gets to create a node because the program just stops. So this function can't parse censored words either.
    @unittest.expectedFailure
    def test_censored_words(self):
        old_nodes = [TextNode("b****", TextType.BOLD)]
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

    def test_no_delimiter(self):
        old_nodes = [TextNode("I forgot to put italic", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes, old_nodes)

    def test_empty_old_nodes(self):
        old_nodes = []
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
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


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and [another link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_image_head(self):
        node = TextNode(
            "![image upfront](https://i.imgur.com/zjjcJKZ.png) and nothing after!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image upfront", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and nothing after!", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_split_image_tail(self):
        node = TextNode(
            "The text comes first and the ![image comes last](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("The text comes first and the ", TextType.TEXT),
                TextNode("image comes last", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),

            ],
            new_nodes,
        )

    def test_split_link_head(self):
        node = TextNode(
            "[link upfront](https://i.imgur.com/zjjcJKZ.png) and nothing after!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link upfront", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and nothing after!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_tail(self):
        node = TextNode(
            "The text comes first and the [link comes last](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("The text comes first and the ", TextType.TEXT),
                TextNode("link comes last", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),

            ],
            new_nodes,
        )

    def test_split_image_no_alt_text(self):
        node = TextNode(
            "I forgot to add alt text ![](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("I forgot to add alt text ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),

            ],
            new_nodes,
        )

    def test_split_link_no_alt_text(self):
        node = TextNode(
            "I forgot to add alt text[](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("I forgot to add alt text", TextType.TEXT),
                TextNode("", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),

            ],
            new_nodes,
        )

    def test_split_image_no_image(self):
        node = TextNode(
            "The markdown for image in this text is absent! https://i.imgur.com/zjjcJKZ.png",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("The markdown for image in this text is absent! https://i.imgur.com/zjjcJKZ.png", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_no_link(self):
        node = TextNode(
            "The markdown for link in this text is absent! https://i.imgur.com/zjjcJKZ.png",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("The markdown for link in this text is absent! https://i.imgur.com/zjjcJKZ.png", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_other_node_type(self):
        node = TextNode(
            "![I'm already an image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.IMAGE,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("![I'm already an image](https://i.imgur.com/zjjcJKZ.png)", TextType.IMAGE),
            ],
            new_nodes,
        )

    def test_split_link_other_node_type(self):
        node = TextNode(
            "[I'm already a link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.LINK,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("[I'm already a link](https://i.imgur.com/zjjcJKZ.png)", TextType.LINK),
            ],
            new_nodes,
        )

# Text to TextNodes suite

    def test_text_to_nodes_all_types(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_text_to_nodes_reverse_order(self):
        text = "[link](https://boot.dev)![image](https://boot.dev)`code`_italic_**bold**"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode("image", TextType.IMAGE, "https://boot.dev"),
                TextNode("code", TextType.CODE),
                TextNode("italic", TextType.ITALIC),
                TextNode("bold", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_text_to_nodes_zero_markdown(self):
        text = "This text has zero markdown."
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This text has zero markdown.", TextType.TEXT)
            ],
            new_nodes
        )

# This test is not necessary, it was only an experiment. It shows the limitation of this simple function.
# With a program written to always treat a _ like a markdown delimiter, and without context awareness,
# it won't ever parse an email address like this correctly. Even with a single _, the program will stop because
# split_nodes_delimiter is always looking for a closing delimiter. And I learned something new about unittest.
    @unittest.expectedFailure
    def test_ambiguous_delimiter(self):
        text = "This is my email: lesson_tester_dev@gmail.com"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is my email: lesson_tester_dev@gmail.com", TextType.TEXT)
            ],
            new_nodes
        )


if __name__ == "__main__":
    unittest.main()
