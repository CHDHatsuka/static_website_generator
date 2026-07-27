import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
# HTMLNode tests
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
# LeafNode tests
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

# ParentNode tests

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_great_grandchildren(self):
        great_grandchild_node = LeafNode("i", "greatgrandchild")
        grandchild_node = ParentNode("b", [great_grandchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b><i>greatgrandchild</i></b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        child_node = LeafNode("span", "child")
        other_child_node = LeafNode("b", "other child")
        parent_node = ParentNode("div", [child_node, other_child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><b>other child</b></div>")

    def test_to_html_with_multiple_mixed_children(self):
        child_node = LeafNode("span", "child")
        cousin_node = LeafNode("i", "I'm the child of the youngest")
        other_child_node = ParentNode("b", [cousin_node])
        parent_node = ParentNode("div", [child_node, other_child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><b><i>I'm the child of the youngest</i></b></div>")

    def test_parent_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_to_html_no_child(self):
        node = ParentNode("b", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_to_html_props(self):
        child_node = LeafNode("span", "child")
        test_props = {
            "href": "https://www.reddit.com",
            "target": "_blank",
        }
        node = ParentNode("a", [child_node], test_props)
        self.assertEqual(node.to_html(), "<a href=\"https://www.reddit.com\" target=\"_blank\"><span>child</span></a>")

    def test_parent_to_html_children_empty(self):
        child_node = []
        node = ParentNode("b", child_node)
        self.assertEqual(node.to_html(), "<b></b>")



if __name__ == "__main__":
    unittest.main()
