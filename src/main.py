from textnode import TextNode, TextType
from functions import split_nodes_delimiter, copy_directories, generate_page_recursive
import os


def main():

    # text_node_0 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    # print(text_node_0)

    source = "static"
    target = "public"
    copy_directories(source, target)
    
    from_path = "content"
    template_path = "template.html"
    dest_path = "public"
    generate_page_recursive(from_path, template_path, dest_path)

if __name__ == "__main__":
    main()