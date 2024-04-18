import unittest

from textnode import TextNode, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
        
    def test_url_none(self):
        node = TextNode("This is a text node", "bold", None)
        node2 = TextNode("This is a text node", "bold", None)
        self.assertEqual(node, node2)    
        
    def test_not_eq(self):
        node = TextNode("This is a text node", "bold", "test")
        node2 = TextNode("This is different", "bold", "test")
        node3 = TextNode("This is different", "italic", "test")
        node4 = TextNode("This is different", "italic", "different")                  
        self.assertNotEqual(node, node2)    
        self.assertNotEqual(node2, node3)  
        self.assertNotEqual(node3, node4)                             
 

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_backtick(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_bold(self):
        node = TextNode("This is text with a **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("bolded", text_type_bold),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(new_nodes, expected)
        
        
    def test_italic(self):
        node = TextNode("This is text with a *italized* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("italized", text_type_italic),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(new_nodes, expected)     
        
    def test_italic_multi(self):
        node = TextNode("This *is text* with a *italized* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        expected = [
            TextNode("This ", text_type_text),
            TextNode("is text", text_type_italic),
            TextNode(" with a ", text_type_text),
            TextNode("italized", text_type_italic),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(new_nodes, expected)                

    def test_backtick_error(self):
        node = TextNode("This is text with a `code block word", text_type_text)
        
        self.assertRaises(
            Exception, 
            split_nodes_delimiter,
            ([node], "`", text_type_code),
            "Matching delimiter not found; invalid Markdown syntax"
            )

class TestExtractMarkdown(unittest.TestCase):
    def test_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        result = extract_markdown_images(text)
        expected = [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]
        self.assertEqual(result, expected)

    def test_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        result = extract_markdown_links(text)
        expected = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
        self.assertEqual(result, expected)        

class TestSplitImages(unittest.TestCase):
    def test_single_image(self):
        node = TextNode(
            "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
            text_type_text,
        )   
        new_nodes = split_nodes_image([node])
        expected = [TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png")]
        self.assertEqual(new_nodes, expected)
        
    def test_image_text_image(self):
        node = TextNode(
            "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        expected = [TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
        TextNode(" and another ", text_type_text),
        TextNode(
            "second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
        )]
        self.assertEqual(new_nodes, expected)
        
    def test_text_after_final_image(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) and a little bit more",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
            ),
            TextNode(" and a little bit more", text_type_text),
            ]
        self.assertEqual(new_nodes, expected)        
        
class TestSplitLinks(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)",
            text_type_text
            )
        new_nodes = split_nodes_link([node])
        expected = [TextNode("This is text with a ", text_type_text),
        TextNode("link", text_type_link, "https://www.example.com"),
        TextNode(" and ", text_type_text),
        TextNode("another", text_type_link, "https://www.example.com/another"
        )]        
        self.assertEqual(new_nodes, expected)

    def test_single_link(self):
        node = TextNode(
            "[link](https://www.example.com)",
            text_type_text
            )
        new_nodes = split_nodes_link([node])
        expected = [
        TextNode("link", text_type_link, "https://www.example.com"),
        ]        
        self.assertEqual(new_nodes, expected)
        
    def test_text_after_final_link(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another) and a little bit more",
            text_type_text
            )
        new_nodes = split_nodes_link([node])
        expected = [TextNode("This is text with a ", text_type_text),
        TextNode("link", text_type_link, "https://www.example.com"),
        TextNode(" and ", text_type_text),
        TextNode("another", text_type_link, "https://www.example.com/another"
        ),
        TextNode(" and a little bit more", text_type_text),]        
        self.assertEqual(new_nodes, expected)
        
    def test_only_multi_links(self):
        node = TextNode(
            "[link](https://www.example.com)[another](https://www.example.com/another)[final](https://www.example.com/final)",
            text_type_text
            )
        new_nodes = split_nodes_link([node])
        expected = [
        TextNode("link", text_type_link, "https://www.example.com"),
        TextNode("another", text_type_link, "https://www.example.com/another"),
        TextNode("final", text_type_link, "https://www.example.com/final"),]        
        self.assertEqual(new_nodes, expected)        

class TestTextToTextNode(unittest.TestCase):
    def test_text_to_text_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        self.assertEqual(result, expected)

    def test_missing_elements(self):
        text = "This is text with an *italic* word and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a little bit more"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a little bit more", text_type_text),
        ]
        self.assertEqual(result, expected)        
   
if __name__ == "__main__":
    unittest.main()
