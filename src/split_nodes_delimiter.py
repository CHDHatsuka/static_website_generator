from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            sections = old_node.text.split(delimiter)
            if len(sections) % 2 == 0:
                raise Exception("missing closing delimiter")
            for index, section in enumerate(sections):
                if section == "":
                    continue
                if index % 2 == 0:
                    new_nodes.append(TextNode(section, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(section, text_type))
    return new_nodes
