from enum import Enum

class TextType(Enum):
    TEXT = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text_content: str, text_type: TextType, url=None):
        self.text = text_content
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        text = self.text
        text_type = self.text_type.value
        url = self.url
        return f"TextNode({text}, {text_type}, {url})"
