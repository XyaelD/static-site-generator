import unittest

from block_markdown import markdown_to_blocks, block_to_block_type, markdown_to_html_node
from block_markdown import (
    block_type_unordered_list,
    block_type_code,
    block_type_heading,
    block_type_ordered_list,
    block_type_paragraph,
    block_type_quote
)
from block_markdown import (
    paragraph_to_html_node,
    heading_to_html_node,
    quote_to_html_node,
    code_to_html_node,
    ordered_list_to_html_node,
    unordered_list__to_html_node
)

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""
        result = markdown_to_blocks(markdown)
        expected = [
            'This is **bolded** paragraph', 
            'This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line', 
            '* This is a list\n* with items'
            ]
        self.assertEqual(result, expected)
        
    def test_markdown_to_blocks_extra_lines(self):
        markdown = """
This is **bolded** paragraph



This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line




* This is a list
* with items
"""
        result = markdown_to_blocks(markdown)
        expected = [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ]
        self.assertEqual(result, expected)
        
class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type(self):
        heading = "### This is a heading"
        heading_wrong = "##This is a wrong heading"
        heading_wrong2 = "######## This is a wrong heading"
        code = "```This is a bunch of code ```"
        code_wrong = "`` Not enough backticks ``"
        quote = ">This is a quote\n>That continues\n>For some more lines"
        quote_wrong = ">This is a wrong quote\nThat continues\nFor some more lines"
        unordered = "*Cats\n*Dogs\n*Fish\n*Birds"
        unordered2 = "-Cats\n-Dogs\n-Fish\n-Birds"
        unordered_wrong = "*Cats\nDogs\n Fish\n-Birds"
        ordered = "1.Cats\n2.Dogs\n3.Fish\n4.Birds"
        ordered_wrong = "1  Cats\n2  Dogs\n3Fish\n4.Birds"
        paragraph = "Nothing special\nSo just a paragraph\n123"
        
        self.assertEqual(block_to_block_type(heading), block_type_heading)
        self.assertEqual(block_to_block_type(heading_wrong), block_type_paragraph)
        self.assertEqual(block_to_block_type(heading_wrong2), block_type_paragraph)
        self.assertEqual(block_to_block_type(code), block_type_code)
        self.assertEqual(block_to_block_type(code_wrong), block_type_paragraph)
        self.assertEqual(block_to_block_type(quote), block_type_quote)
        self.assertEqual(block_to_block_type(quote_wrong), block_type_paragraph)
        self.assertEqual(block_to_block_type(unordered), block_type_unordered_list)
        self.assertEqual(block_to_block_type(unordered2), block_type_unordered_list)
        self.assertEqual(block_to_block_type(unordered_wrong), block_type_paragraph)
        self.assertEqual(block_to_block_type(ordered), block_type_ordered_list)
        self.assertEqual(block_to_block_type(ordered_wrong), block_type_paragraph)
        self.assertEqual(block_to_block_type(paragraph), block_type_paragraph)        
        
class BlocksToHtmlNodes(unittest.TestCase):
    def test_paragraph(self):
        paragraph = "Nothing special\nSo just a paragraph\nWith a **bolded** word!"
        test = paragraph_to_html_node(paragraph)
    
    def test_heading(self):
        heading = "### This is a *heading*"
        test = heading_to_html_node(heading)
    
    def test_quote(self):
        quote = ">This is a quote\n>That continues\n>For some more lines"
        test = quote_to_html_node(quote)
          
    def test_code(self):
        code = "```This is a bunch of code```"
        test = code_to_html_node(code)
        
    def test_ordered(self):
        ordered = "1.Cats\n2.Dogs\n3.Fish\n4.Birds"
        test = ordered_list_to_html_node(ordered)
        
    def test_unordered(self):
        unordered = "*Cats\n*Dogs\n*Fish\n*Birds"
        unordered2 = "-Cats\n-Dogs\n-Fish\n-Birds"
        
        test = unordered_list__to_html_node(unordered)
        test2 = unordered_list__to_html_node(unordered2)
    
    def test_markdown_to_html_node(self):
        markdown = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""

        test = markdown_to_html_node(markdown)
        print(test)           