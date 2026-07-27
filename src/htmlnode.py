
class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list["HTMLNode"] = None, props: dict[str, str] = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
        # Subclasses should implement this themselves

    def props_to_html(self) -> str:
        if not self.props:
            return ""

        formatted_str = ""
        for k, v in self.props.items():
            formatted_str += f" {k}=\"{v}\""
        return formatted_str

    def __repr__(self) -> str:
        return f"HTMLNode tag = {self.tag}, value = {self.value}, children = {self.children}, props = {self.props}"

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict[str, str] = None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"HTMLNode tag = {self.tag} value = {self.value}, props = {self.props}"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list["HTMLNode"], props: dict[str, str] = None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag == None:
            raise ValueError("tag is required")
        if self.children == None:
            raise ValueError("children is required")
        else:
            child_html = ""
            for child in self.children:
                child_html += child.to_html()
            return f"<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>"
