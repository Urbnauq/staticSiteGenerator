from textnode import TextNode, TextType, DELIMITERS
from htmlnode import HTMLNode, ParentNode, LeafNode
import re
from enum import Enum

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

# Block_to_block_type-------------------------------------------------------------------------------
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    headings = {
        "#" : "#",
        "##" : "##",
        "###" : "###",
        "####" : "####",
        "#####" : "#####",
        "######" : "######"
    }

    lines = block.split("\n")

    if (block.startswith("#")):
        heading = block.split(" ", maxsplit=1)[0]
        if (headings.get(heading)):
            return BlockType.HEADING
        else:
            return BlockType.PARAGRAPH
    
    if (block[:3] == "```" and block[-3:] == "```" ):
        return BlockType.CODE
    
    if (block[:1] == ">"):
        for line in lines:
            if (line[:1] != ">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    if (block[:2] == "- "):
        for line in lines:
            if (line[:2] !=  "- "):
                return BlockType.PARAGRAPH    
        return BlockType.UNORDERED_LIST
    
    if (block[:3] == "1. "):
        i = 1
        for line in lines:
            if (line[:3] != f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

# Markdown_to_HTML_Node-------------------------------------------------------------------------------

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block_to_html = block_to_html_node(block, block_type)
        children.append(block_to_html)
        
    node_html = ParentNode("div", children, None)
    return node_html

    # Helpers---------------------------
def block_to_html_node(text, block_type):
    if block_type == BlockType.PARAGRAPH: 
        return ParentNode("p", text_to_children(text.replace("\n", " ")))
    if block_type == BlockType.HEADING: 
        return ParentNode(heading_tag(text)[0], text_to_children(heading_tag(text)[1].replace("\n", " ")))
    if block_type == BlockType.CODE: 
        return ParentNode("pre", [ParentNode("code", [text_node_to_html_node(TextNode(code_text(text), TextType.TEXT))])])
    if block_type == BlockType.QUOTE:
        return ParentNode("blockquote", text_to_children(text.replace(">", "").lstrip(" ")))
    if block_type == BlockType.UNORDERED_LIST:
        return ParentNode("ul", unordered_list(text))
    if BlockType.ORDERED_LIST:
        return ParentNode("ol", ordered_list(text))

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return children

def heading_tag(text):
    heading_dic = {
        "#" : "h1",
        "##" : "h2",
        "###" : "h3",
        "####" : "h4",
        "#####" : "h5",
        "######" : "h6"
        }
    
    heading = text.split(" ", maxsplit=1)
    
    if heading_dic.get(heading[0]):
        return heading_dic.get(heading[0]), heading[1]
    return text

def code_text(text):
    return text.replace("```", "").lstrip("\n")

def unordered_list(text):
    unordered_split = text.split("\n")
    print(unordered_split)
    parents = []
    for lst in unordered_split:
        if lst == "":
            continue
        text_formated = lst.replace("-", "").lstrip(" ")
        parents.append(ParentNode("li", text_to_children(text_formated)))
    return parents

def ordered_list(text):
    ordered_split = text.split("\n")
    parents = []
    for lst in ordered_split:
        if lst == "":
            continue
        text_formated = lst.replace(lst[:2], "").lstrip(" ")
        parents.append(ParentNode("li", text_to_children(text_formated)))
    return parents
    
