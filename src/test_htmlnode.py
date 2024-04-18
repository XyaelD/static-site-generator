import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        converted_node = node.props_to_html()
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(converted_node, expected)
        
        not_expected = 'href="https://www.google.com" target="_blank"'
        self.assertNotEqual(converted_node, not_expected)
        
class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        converted = node.to_html()
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        converted2 = node2.to_html()
        node3 = LeafNode(None, "Click me!", {"href": "https://www.google.com"})
        converted3 = node3.to_html()
        
        expected = "<p>This is a paragraph of text.</p>"
        expected2 = '<a href="https://www.google.com">Click me!</a>'
        expected3 = 'Click me!'
                
        self.assertEqual(converted, expected)
        self.assertEqual(converted2, expected2)
        self.assertEqual(converted3, expected3)                

class TestParentNode(unittest.TestCase):
    def test_parent_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(node.to_html(), expected)
        
        nested_parent = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                ),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected_nested_parent = '<p><b>Bold text</b>Normal text<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><i>italic text</i>Normal text</p>'        
        self.assertEqual(nested_parent.to_html(), expected_nested_parent)

        nested_same_level = ParentNode(
            "p",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                    ],
                ),
                ParentNode(
                    "p",
                    [
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                ),  
            ],
        )
        
        expected_nested_same_level = '<p><p><b>Bold text</b>Normal text</p><p><i>italic text</i>Normal text</p></p>'
        self.assertEqual(nested_same_level.to_html(), expected_nested_same_level)
                           
if __name__ == "__main__":
    unittest.main()
