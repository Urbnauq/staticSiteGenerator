from textnode import TextNode, TextType, DELIMITERS
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
    links = []
    for match in matches:
        alt = re.findall(r"\[(.*?)\]", match)[0]
        link = re.findall(r"\((.*?)\)", match)[0]
        links.append((alt, link))
    return links

# Split_nodes_images & Split_nodes_links-------------------------------------------------------------------------------
def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        images = extract_markdown_images(node.text)
        original_text = node.text

        if images == []:
            new_nodes.append(node)
            continue

        if original_text == "":
            continue
        
        for image in images:
            image_alt = image[0]
            image_link = image[1]
            
            sections = original_text.split(f"![{image_alt}]({image_link})", 1)

            if len(sections) != 2:
                raise ValueError("Invalid image markdown")
            
            original_text = sections[1]

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
    
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        links = extract_markdown_links(node.text)
        original_text = node.text

        if links == []:
            new_nodes.append(node)
            continue

        if original_text == "":
            continue
        
        for link in links:
            alt = link[0]
            link_ = link[1]
            
            sections = original_text.split(f"[{alt}]({link_})", 1)
            
            if len(sections) != 2:
                raise ValueError("Invalid link markdown")
            
            original_text = sections[1]
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            new_nodes.append(TextNode(alt, TextType.LINK, link_))
    
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

# Text_to_textnodes-------------------------------------------------------------------------------
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    for delimiter in DELIMITERS:
        nodes = split_nodes_delimiter(nodes, DELIMITERS[delimiter], delimiter)

    split_nodes_image_and_link = [split_nodes_image, split_nodes_link]
    for split_node in split_nodes_image_and_link:
        nodes = split_node(nodes)
    
    return nodes

# Markdown_to_blocks-------------------------------------------------------------------------------
def markdown_to_blocks(markdown):
    md = markdown.split("\n\n")
    blocks = []
    
    for i in range(len(md)):
        if md[i] == "":
            continue
        else:
            blocks.append(md[i].strip())
        
    return blocks