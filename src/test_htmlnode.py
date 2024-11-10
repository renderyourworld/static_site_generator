import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_empty(self):
        node = HTMLNode()
        self.assertEqual([node.tag, node.value, node.children, node.props], [None, None, None, None])
    
    def test_repr(self):
        node = HTMLNode("p", "Hello", None, {"class": "primary"})
        self.assertEqual(repr(node), "HTMLNode(p, Hello, children: None, {'class': 'primary'})")

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
        node = LeafNode(None, "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), 'Click me!')

class TestParentNode(unittest.TestCase):
    def test_nested_parents(self):
        inner_parent = ParentNode("p", [LeafNode("b", "Bold text")])
        outer_parent = ParentNode("div", [inner_parent])
        self.assertEqual(outer_parent.to_html(), "<div><p><b>Bold text</b></p></div>")
    
    def test_multiple_children(self):
        node = ParentNode("p", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text")])
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text</p>")

    def test_no_children(self):
        node = ParentNode("p", [])
        self.assertEqual(node.to_html(), "<p></p>")

if __name__ == "__main__":
    unittest.main()