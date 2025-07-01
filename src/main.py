from textnode import TextNode, TextType
from functions import split_nodes_delimiter, copy_directories, generate_page


def main():

    # text_node_0 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    # print(text_node_0)

    source = "static"
    target = "public"
    copy_directories(source, target)
    
    from_path = "content/index.md"
    template_path = "template.html"
    dest_path = None
    generate_page(from_path, template_path, dest_path)

    # Checkpoint - CH3:L5
if __name__ == "__main__":
    main()