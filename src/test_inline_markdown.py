import unittest
from inline_markdown import extract_markdown_images, extract_markdown_links

class TestHTMLNode(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is a link to [Reddit](https://www.reddit.com)!"
        )
        self.assertListEqual(
            [
                ("Reddit","https://www.reddit.com")
            ],
            matches
        )

    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
            "This text has ![img1](https://i.imgur.com/zjjcJKZ.png) and ![img2](https://i.imgur.com/zjjc000.png)"
        )
        self.assertListEqual(
            [("img1", "https://i.imgur.com/zjjcJKZ.png"),
            ("img2", "https://i.imgur.com/zjjc000.png"),
            ],
            matches
        )

    def test_extract_multiple_links(self):
        matches = extract_markdown_links(
            "This text has [link1](https://www.reddit.com) and [link2](https://www.reddit.com)!"
        )
        self.assertListEqual(
            [
                ("link1", "https://www.reddit.com"),
                ("link2", "https://www.reddit.com"),
            ],
            matches
        )

    def test_extract_only_img(self):
        matches = extract_markdown_images(
            "This text has ![an img](https://i.imgur.com/zjjcJKZ.png) and [a link](https://www.reddit.com)"
        )
        self.assertListEqual(
            [
                ("an img", "https://i.imgur.com/zjjcJKZ.png"),
            ],
            matches
        )

    def test_extract_only_text(self):
        matches = extract_markdown_links(
            "This text has ![an img](https://i.imgur.com/zjjcJKZ.png) and [a link](https://www.reddit.com)"
        )
        self.assertListEqual(
            [
                ("a link", "https://www.reddit.com"),
            ],
            matches
        )

    def test_empty_img_alt(self):
        matches = extract_markdown_images(
            "I forgot to add alt text ![](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [
                ("", "https://i.imgur.com/zjjcJKZ.png"),
            ],
            matches
        )

    def test_empty_img_url(self):
        matches = extract_markdown_images(
            "I forgot to add url ![oh no]()"
        )
        self.assertListEqual(
            [
                ("oh no", ""),
            ],
            matches
        )

    def test_empty_link_text(self):
        matches = extract_markdown_links(
            "I forgot to add text [](https://www.reddit.com)"
        )
        self.assertListEqual(
            [
                ("", "https://www.reddit.com"),
            ],
            matches
        )

    def test_empty_link_url(self):
        matches = extract_markdown_links(
            "I forgot to add url [oh no]()"
        )
        self.assertListEqual(
            [
                ("oh no", ""),
            ],
            matches
        )

if __name__ == "__main__":
    unittest.main()
