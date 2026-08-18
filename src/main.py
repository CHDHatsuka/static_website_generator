from textnode import TextNode
from textnode import TextType
from copystatic import copystatic
from gencontent import generate_page, generate_pages_recursive

source_path = "./static"
destination_path = "./public"
from_path = "./content"
template_path = "./template.html"
dest_path = "./public"

# If the program was a factory, main.py is the operation instructions for a machine that sits in a separate room (main.sh)
# so the paths we assign to variables start assume the POV of the machine, not of the file cabinet where the operations are stored.
def main() -> None:
    copystatic(source_path, destination_path)
    generate_pages_recursive(from_path, template_path, dest_path)


main()
