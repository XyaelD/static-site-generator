import unittest
from generate_html import extract_title

class TestGenerateHTML(unittest.TestCase):
    def test_extract_title(self):
        markdown = """# This is the title!

This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items

1. And an
2. Ordered list"""

        title = extract_title(markdown)
        expected = "This is the title!"
        self.assertEqual(title, expected)
        
    def test_no_title(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items

1. And an
2. Ordered list"""

        self.assertRaises(
            Exception, 
            extract_title,
            (markdown),
            "No title in the markdown! At least one h1 element is required!"
            )
        
if __name__ == "__main__":
    unittest.main()