
class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list["HTMLNode"] = None, props: dict[str, str] = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html():
        raise Exception(NotImplementedError)

    def props_to_html(self) -> str:
        if not self.props:
            return ""

        formatted_str = ""
        for k, v in self.props.items():
            formatted_str += f" {k}=\"{v}\""
        return formatted_str

    def __repr__(self) -> str:
        return f"HTMLNode tag = {self.tag}, " + f"value = {self.value}, " + f"children = {self.children}, " + f"props = {self.props}"
