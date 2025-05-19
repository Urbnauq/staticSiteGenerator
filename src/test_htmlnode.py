import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

    # ParentNode-------------------------------------------------------------------------------------
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
    
    def test_to_html_with_grandchildren_PROPS(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("a", [grandchild_node], PROPS)
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><a href="https://www.google.com" target="_blank"><b>grandchild</b></a></div>',
        )

if __name__ == "__main__":
    unittest.main()