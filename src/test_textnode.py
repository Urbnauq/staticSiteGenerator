import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_no_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node2", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_is_node(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertIsNone(node.url)

if __name__ == "__main__":
    unittest.main()