from textnode import TextNode, TextType
from functions import split_nodes_delimiter, copy_directories


def main():

    # text_node_0 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    # print(text_node_0)

    source = "static"
    target = "public"
    copy_directories(source, target)

    # Checkpoint - CH3:L5
if __name__ == "__main__":
    main()