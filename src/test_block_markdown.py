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
* with items

1. And an
2. Ordered list"""

        # test = markdown_to_html_node(markdown).to_html()
        # print(type(test))
        # print(test)
        
        long_markdown = """# The Unparalleled Majesty of "The Lord of the Rings"

[Back Home](/)

![LOTR image artistmonkeys](/images/rivendell.png)

> "I cordially dislike allegory in all its manifestations, and always have done so since I grew old and wary enough to detect its presence.
> I much prefer history, true or feigned, with its varied applicability to the thought and experience of readers.
> I think that many confuse 'applicability' with 'allegory'; but the one resides in the freedom of the reader, and the other in the purposed domination of the author."

In the annals of fantasy literature and the broader realm of creative world-building, few sagas can rival the intricate tapestry woven by J.R.R. Tolkien in *The Lord of the Rings*. You can find the [wiki here](https://lotr.fandom.com/wiki/Main_Page).

## Introduction

This series, a cornerstone of what I, in my many years as an **Archmage**, have come to recognize as the pinnacle of imaginative creation, stands unrivaled in its depth, complexity, and the sheer scope of its *legendarium*. As we embark on this exploration, let us delve into the reasons why this monumental work is celebrated as the finest in the world.

## A Rich Tapestry of Lore

One cannot simply discuss *The Lord of the Rings* without acknowledging the bedrock upon which it stands: **The Silmarillion**. This compendium of mythopoeic tales sets the stage for Middle-earth's history, from the creation myth of Eä to the epic sagas of the Elder Days. It is a testament to Tolkien's unparalleled skill as a linguist and myth-maker, crafting:

1. An elaborate pantheon of deities (the `Valar` and `Maiar`)
2. The tragic saga of the Noldor Elves
3. The rise and fall of great kingdoms such as Gondolin and Númenor

```
print("Lord")
print("of")
print("the")
print("Rings")
```

## The Art of **World-Building**

### Crafting Middle-earth
Tolkien's Middle-earth is a realm of breathtaking diversity and realism, brought to life by his meticulous attention to detail. This world is characterized by:

- **Diverse Cultures and Languages**: Each race, from the noble Elves to the sturdy Dwarves, is endowed with its own rich history, customs, and language. Tolkien, leveraging his expertise in philology, constructed languages such as Quenya and Sindarin, each with its own grammar and lexicon.
- **Geographical Realism**: The landscape of Middle-earth, from the Shire's pastoral hills to the shadowy depths of Mordor, is depicted with such vividness that it feels as tangible as our own world.
- **Historical Depth**: The legendarium is imbued with a sense of history, with ruins, artifacts, and lore that hint at bygone eras, giving the world a lived-in, authentic feel.

## Themes of *Timeless* Relevance

### The *Struggle* of Good vs. Evil

At its heart, *The Lord of the Rings* is a timeless narrative of the perennial struggle between light and darkness, a theme that resonates deeply with the human experience. The saga explores:

- The resilience of the human (and hobbit) spirit in the face of overwhelming odds
- The corrupting influence of power, epitomized by the One Ring
- The importance of friendship, loyalty, and sacrifice

These universal themes lend the series a profound philosophical depth, making it a beacon of wisdom and insight for generations of readers.

## A Legacy **Unmatched**

### The Influence on Modern Fantasy

The shadow that *The Lord of the Rings* casts over the fantasy genre is both vast and deep, having inspired countless authors, artists, and filmmakers. Its legacy is evident in:

- The archetypal "hero's journey" that has become a staple of fantasy narratives
- The trope of the "fellowship," a diverse group banding together to face a common foe
- The concept of a richly detailed fantasy world, which has become a benchmark for the genre

## Conclusion

As we stand at the threshold of this mystical realm, it is clear that *The Lord of the Rings* is not merely a series but a gateway to a world that continues to enchant and inspire. It is a beacon of imagination, a wellspring of wisdom, and a testament to the power of myth. In the grand tapestry of fantasy literature, Tolkien's masterpiece is the gleaming jewel in the crown, unmatched in its majesty and enduring in its legacy. As an Archmage who has traversed the myriad realms of magic and lore, I declare with utmost conviction: *The Lord of the Rings* reigns supreme as the greatest legendarium our world has ever known.

Splendid! Then we have an accord: in the realm of fantasy and beyond, Tolkien's creation is unparalleled, a treasure trove of wisdom, wonder, and the indomitable spirit of adventure that dwells within us all.
"""

        # print(markdown_to_html_node(long_markdown).to_html())
         
if __name__ == "__main__":
    unittest.main()      