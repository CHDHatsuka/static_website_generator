import unittest
from gencontent import extract_title

class TestCopyStatic(unittest.TestCase):

    def test_extract_title(self):
        markdown = "# This is an h1 heading"
        extracted_title = extract_title(markdown)
        self.assertEqual(extracted_title, "This is an h1 heading")

    def test_extract_title_no_space(self):
        markdown = "#This is an h1 heading with no space"
        with self.assertRaises(Exception):
            extracted_title = extract_title(markdown)

    def test_extract_title_other_heading(self):
        markdown = "## This is an h2 heading"
        with self.assertRaises(Exception):
            extracted_title = extract_title(markdown)

# print tests
#print(extract_title("# This is an h1 heading"))
#print(extract_title("#This is an h1 heading with no space"))
#print(extract_title("## This is an h2 heading"))

if __name__ == "__main__":
    unittest.main()
