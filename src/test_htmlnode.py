import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_good_props_to_html(self):
        sample_list = ["pretend there's a node here", "pretend there's another node here"]
        good_props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node1 = HTMLNode("node1", "this is node 1", sample_list, good_props)
        answer = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(node1.props_to_html(), answer)

    def test_empty_props_to_html(self):
        sample_list = ["pretend there's a node here", "pretend there's another node here"]
        empty_props = {}
        node1 = HTMLNode("node1", "this is node 1", sample_list, empty_props)
        answer = ""
        self.assertEqual(node1.props_to_html(), answer)

    def test_props_is_none(self):
        sample_list = ["pretend there's a node here", "pretend there's another node here"]
        node1 = HTMLNode("node1", "this is node 1", sample_list)
        answer = ""
        self.assertEqual(node1.props_to_html(), answer)

    def test_repr(self):
        node1 = HTMLNode("node1", "node1")
        answer = "HTMLNode tag = node1, value = node1, children = None, props = None"
        self.assertEqual(node1.__repr__(), answer)

    def test_repr_none(self):
        node1 = HTMLNode()
        answer = "HTMLNode tag = None, value = None, children = None, props = None"
        self.assertEqual(node1.__repr__(), answer)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_props(self):
        test_props = {
            "href": "https://www.reddit.com",
            "target": "_blank",
        }
        node = LeafNode("a", "Reddit", test_props)
        self.assertEqual(node.to_html(), "<a href=\"https://www.reddit.com\" target=\"_blank\">Reddit</a>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "I put no HTML tags around this text", None)
        self.assertEqual(node.to_html(), "I put no HTML tags around this text")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None, None)
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()
