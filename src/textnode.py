from htmlnode import LeafNode
import re

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        
    def __eq__(self, other):
        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
      ):  
            return True
        else:
            return False
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type == text_type_text:
        return LeafNode(value=text_node.text)
    elif text_node.text_type == text_type_bold:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == text_type_italic:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == text_type_code:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == text_type_link:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == text_type_image:
        return LeafNode(tag="img", value=None, props={"src": text_node.url, "alt": text_node.text}) 
    raise Exception("Not a valid type of TextNode")

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) == 1:
                new_nodes.append(node)
                continue
            if len(split_text) % 2 != 1:
                raise Exception("Matching delimiter not found; invalid Markdown syntax")
            for i in range(len(split_text)):
                if i % 2 == 0:
                    new_nodes.append(TextNode(split_text[i], text_type_text))
                else:
                    new_nodes.append(TextNode(split_text[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches
    
def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        else:
            image_tuples = extract_markdown_images(node.text)
            text_copy = node.text
            if len(image_tuples) == 0:
                new_nodes.append(node)
                continue
            for image in image_tuples:
                split_text = text_copy.split(f"![{image[0]}]({image[1]})", 1)
                if split_text[0] != "":
                    new_nodes.append(TextNode(split_text[0], text_type_text))
                new_nodes.append(TextNode(image[0], text_type_image, image[1]))
                text_copy = split_text[1]
            # If there was another text element after the last image, add it
            if text_copy != "":
                new_nodes.append((TextNode(text_copy, text_type_text)))   
    return new_nodes         

def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        else:
            link_tuples = extract_markdown_links(node.text)
            text_copy = node.text
            if len(link_tuples) == 0:
                new_nodes.append(node)
                continue
            for link in link_tuples:
                split_text = text_copy.split(f"[{link[0]}]({link[1]})", 1)
                if split_text[0] != "":
                    new_nodes.append(TextNode(split_text[0], text_type_text))
                new_nodes.append(TextNode(link[0], text_type_link, link[1]))
                text_copy = split_text[1]
            # If there was another text element after the last link, add it
            if text_copy != "":
                new_nodes.append((TextNode(text_copy, text_type_text)))   
    return new_nodes                                  

def text_to_textnodes(text):
    node = TextNode(text, text_type_text)
    initial_nodes = [node]
    text_nodes = split_nodes_delimiter(initial_nodes, '`', text_type_code)
    text_nodes = split_nodes_delimiter(text_nodes, '**', text_type_bold)
    text_nodes = split_nodes_delimiter(text_nodes, '*', text_type_italic)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes