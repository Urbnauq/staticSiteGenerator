from textnode import TextNode, TextType

def main():

    text_node_0 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(text_node_0)

if __name__ == "__main__":
    main()