def extract_title(markdown: str) -> str:
    if not markdown.startswith("# "):
        raise Exception("No h1 header found")
    return markdown.split("# ", maxsplit=1)[1]
