from textnode import TextNode
from textnode import TextType

def main():
    print("hello world")

    dummy = TextNode("dummy text", TextType.BOLD, "https://www.boot.dev")

    print(dummy)

main()
