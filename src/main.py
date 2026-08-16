from textnode import TextNode
from textnode import TextType
from copystatic import copystatic

source_path = "./static"
destination_path = "./public"

def main() -> None:
    copystatic(source_path, destination_path)



main()
