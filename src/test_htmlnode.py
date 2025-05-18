import unittest

from htmlnode import HTMLNode, LeafNode

PROPS = {
    "href": "https://www.google.com",
    "target": "_blank",
    }

class TestHTMLNode(unittest.TestCase):

    def test_HTMLNode_props_to_html_eq(self):
        node = HTMLNode("p", "This is a text node", None, PROPS)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_HTMLNode_props_to_html_is_none(self):
        node = HTMLNode("p", "This is a text node", None, None)
        self.assertEqual(node.props_to_html(), "")

    # LeafNode-------------------------------------------------------------------------------------
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_tag_none(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("p", "Hello, world!", PROPS)
        self.assertEqual(node.to_html(), '<p href="https://www.google.com" target="_blank">Hello, world!</p>')

if __name__ == "__main__":
    unittest.main()