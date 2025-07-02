from functions import copy_directories, generate_page_recursive
import sys

def main():
    print(sys.argv)

    source = "static"
    target = "public"
    copy_directories(source, target)
    
    from_path = "content"
    template_path = "template.html"
    dest_path = "public"
    generate_page_recursive(from_path, template_path, dest_path)

if __name__ == "__main__":
    main()