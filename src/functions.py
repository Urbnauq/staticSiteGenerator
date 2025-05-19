from textnode import TextNode, TextType
from htmlnode import LeafNode
import re

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href" : text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src" : text_node.url, "alt" : text_node.text})
    raise ValueError(f"invalid text type: {text_node.text_type}")

# split_nodes_delimiter-------------------------------------------------------------------------------
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for i in range(len(old_nodes)):
        if old_nodes[i].text_type != TextType.TEXT:
            new_nodes.append(old_nodes[i])
            continue
    
        node_text_split = old_nodes[i].text.split(delimiter)

        if len(node_text_split) % 2 == 0:
            raise ValueError("Invalid Markdown syntax!")
        
        splited_nodes = []
        for j in range(len(node_text_split)):
            if node_text_split[j] == "":
                continue
            
            if j % 2 == 1:
                splited_nodes.append(TextNode(node_text_split[j], text_type))
            else:
                splited_nodes.append(TextNode(node_text_split[j], TextType.TEXT))
        
        new_nodes.extend(splited_nodes)
    
    return new_nodes

# extract_markdown_images & extract_markdown_links-------------------------------------------------------------------------------
def extract_markdown_images(text):
    matches = re.findall(r"!\[.*?\]\(.*?\)", text)
    images = []
    for match in matches:
        alt = re.findall(r"\[(.*?)\]", match)[0]
        image = re.findall(r"\((.*?)\)", match)[0]
        images.append((alt, image))
    return images

def extract_markdown_links(text):
    matches = re.findall(r"\[.*?\]\(.*?\)", text)
    images = []
    for match in matches:
        alt = re.findall(r"\[(.*?)\]", match)[0]
        link = re.findall(r"\((.*?)\)", match)[0]
        images.append((alt, link))
    return images