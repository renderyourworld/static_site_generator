import re
from textnode import *

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        # Split text into sections and create new TextNode
        segments = node.text.split(delimiter)
        if len(segments) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i, segment in enumerate(segments):
            if i % 2 : # Every other item in the list should be inside the delimiter
                new_nodes.append(TextNode(segment, text_type))
            elif segment: # Handle a potential empty segment
                new_nodes.append(TextNode(segment, TextType.TEXT))
    
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        org_text = node.text
        images = extract_markdown_images(org_text)
        if not images:
            new_nodes.append(node)
            continue
        for image in images:
            img_alt = image[0]
            img_link = image[1]
            sections = org_text.split(f"![{img_alt}]({img_link})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(img_alt, TextType.IMAGE, img_link))
            org_text = sections[1]
        if org_text != "":
            new_nodes.append(TextNode(org_text, TextType.TEXT))
    
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        org_text = node.text
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        for link in links:
            link_text = link[0]
            link_url = link[1]
            sections = org_text.split(f"[{link_text}]({link_url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            org_text = sections[1]
        if org_text != "":
            new_nodes.append(TextNode(org_text, TextType.TEXT))
    
    return new_nodes

def extract_markdown_images(text: str) -> list:
	alt_text_pattern = r"!\[(.*?)\]"
	images_pattern = r"\((.*?)\)"
	images = re.findall(f"{alt_text_pattern}{images_pattern}", text)

	return images

def extract_markdown_links(text: str) -> list:
	anchor_text_pattern = r"\[(.*?)\]"
	links_pattern = r"\((.*?)\)"
	links = re.findall(f"{anchor_text_pattern}{links_pattern}", text)

	return links

def text_to_textnodes(text: str) -> list[TextNode]:
    text_nodes = split_nodes_image([TextNode(text, TextType.TEXT)])
    text_nodes = split_nodes_link(text_nodes)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "*", TextType.ITALIC)

    return text_nodes