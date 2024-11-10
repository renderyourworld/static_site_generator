import unittest
from inline_markdown import *
from textnode import *

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
    
    def test_bold(self):
        node = TextNode("This is text with **bold text**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes[1].text, "bold text")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

class TestExtractImages(unittest.TestCase):
    def test_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [("rick roll", "https://i.imgur.com/aKaOqIh.gif")])

class TestExtractLinks(unittest.TestCase):
    def test_links(self):
        text = "This is text with a link [to google](https://www.google.com) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [("to google", "https://www.google.com"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

class TestSplitNodesImage(unittest.TestCase):
    def test_multiple_images(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes,
                         [
                          TextNode("This is text with a ", TextType.TEXT, None), 
                          TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), 
                          TextNode(" and ", TextType.TEXT, None), 
                          TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
                         ])
    
    def test_single_image(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes,
                         [
                          TextNode("This is text with a ", TextType.TEXT, None), 
                          TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), 
                         ])
    
    def test_text(self):
        node = TextNode("This is text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [TextNode("This is text", TextType.TEXT, None)])

class TestSplitNodesLink(unittest.TestCase):
    def test_multiple_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes,
                         [
                          TextNode("This is text with a link ", TextType.TEXT, None), 
                          TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), 
                          TextNode(" and ", TextType.TEXT, None), 
                          TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
                         ])
    
    def test_single_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes,
                         [
                          TextNode("This is text with a link ", TextType.TEXT, None), 
                          TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), 
                         ])
    
    def test_text(self):
        node = TextNode("This is text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [TextNode("This is text", TextType.TEXT, None)])

class TestTextToTextNodes(unittest.TestCase):
    def test_multiple_types(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(new_nodes, 
                         [
                            TextNode('This is ', TextType.TEXT, None),
                            TextNode('text', TextType.BOLD, None),
                            TextNode(' with an ', TextType.TEXT, None),
                            TextNode('italic', TextType.ITALIC, None),
                            TextNode(' word and a ', TextType.TEXT, None),
                            TextNode('code block', TextType.CODE, None),
                            TextNode(' and an ', TextType.TEXT, None),
                            TextNode('obi wan image', TextType.IMAGE, 'https://i.imgur.com/fJRm4Vk.jpeg'),
                            TextNode(' and a ', TextType.TEXT, None),
                            TextNode('link', TextType.LINK, 'https://boot.dev')
                         ])
    
    def test_inline_only(self):
        text = "This is **text** with an *italic* word and a `code block`."
        new_nodes = text_to_textnodes(text)
        self.assertEqual(new_nodes, 
                         [
                            TextNode('This is ', TextType.TEXT, None),
                            TextNode('text', TextType.BOLD, None),
                            TextNode(' with an ', TextType.TEXT, None),
                            TextNode('italic', TextType.ITALIC, None),
                            TextNode(' word and a ', TextType.TEXT, None),
                            TextNode('code block', TextType.CODE, None),
                            TextNode('.', TextType.TEXT, None),
                         ])
        
if __name__ == "__main__":
    unittest.main()