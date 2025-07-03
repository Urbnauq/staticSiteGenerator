from functions import copy_directories, generate_page_recursive
import sys

def main():

    source = "static"
    target = "docs"
    copy_directories(source, target)
    
    from_path = "content"
    template_path = "template.html"
    dest_path = "docs"
    generate_page_recursive(from_path, template_path, dest_path)

if __name__ == "__main__":
    main()