from htmlnode import ParentNode, LeafNode
from textnode import TextNode, text_to_textnodes, text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

def markdown_to_blocks(markdown):
    split_to_blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in split_to_blocks:
        if block == "":
            continue
        cleaned = block.strip()
        cleaned_blocks.append(cleaned)
    return cleaned_blocks

def block_to_block_type(block):
    
    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
        ):
            return block_type_heading
    
    elif block[0] == '`' and block[1] == '`' and block[2] == '`' and block[-1] == '`' and block[-2] == '`' and block[-3] == '`':
        return block_type_code
    lines = block.split("\n")
    
    quote = True
    unordered = True
    ordered = True
    
    for line in lines:
        if line[0] == ">":
            continue
        else:
            quote = False
    if quote:
        return block_type_quote
    
    for line in lines:
        if line[0] == "*" or line[0] == "-":
            continue
        else:
            unordered = False     
    if unordered:
        return block_type_unordered_list
    
    line_count = 1
    for line in lines:
        if line[0] == str(line_count) and line[1] == ".":
            line_count += 1
        else:
            ordered = False
    if ordered:
        return block_type_ordered_list
    
    return block_type_paragraph

# Likely need to replace \n with <br> for html parsing                
def paragraph_to_html_node(block):
    cleaned_block = block.replace("\n", "<br>")
    text_nodes = text_to_textnodes(cleaned_block)
    children = list(map(text_node_to_html_node, text_nodes))
    parent_node = ParentNode(tag="p", children=children)
    return parent_node

def heading_to_html_node(block):
    hash_count = block.count("#")
    cleaned_block = block.replace("#", "").strip()
    text_nodes = text_to_textnodes(cleaned_block)
    children = list(map(text_node_to_html_node, text_nodes))
    parent_node = ParentNode(tag=f"h{hash_count}", children=children)
    return parent_node

def quote_to_html_node(block):
    cleaned_block = block.replace(">", "").replace("\n", "<br>")
    text_nodes = text_to_textnodes(cleaned_block)
    children = list(map(text_node_to_html_node, text_nodes))
    parent_node = ParentNode(tag="blockquote", children=children)
    return parent_node

def code_to_html_node(block):
    cleaned_block = block.replace("`", "").replace("\n", "<br>")
    text_nodes = text_to_textnodes(cleaned_block)
    children = list(map(text_node_to_html_node, text_nodes))
    code_node = ParentNode(tag="code", children=children)
    parent_node = ParentNode(tag="pre", children=code_node)
    return parent_node

def ordered_list_to_html_node(block):
    split_list = block.split("\n")
    readied_list = list(map(lambda x: "<li>" + x[2:] + "</li>", split_list))
    readied_string = "".join(readied_list)
    text_nodes = text_to_textnodes(readied_string)
    children = list(map(text_node_to_html_node, text_nodes))
    parent_node = ParentNode(tag="ol", children=children)
    return parent_node

def unordered_list__to_html_node(block):
    split_list = block.split("\n")
    readied_list = list(map(lambda x: "<li>" + x[1:] + "</li>", split_list))
    readied_string = "".join(readied_list)
    text_nodes = text_to_textnodes(readied_string)
    children = list(map(text_node_to_html_node, text_nodes))
    parent_node = ParentNode(tag="ol", children=children)
    return parent_node

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_types = []
    for block in blocks:
        block_types.append(block_to_block_type(block))
    html_nodes = []
    for i in range(len(blocks)):
        if block_types[i] == block_type_code:
            html_nodes.append(code_to_html_node(blocks[i]))
            
        elif block_types[i] == block_type_paragraph:
            html_nodes.append(paragraph_to_html_node(blocks[i]))
            
        elif block_types[i] == block_type_quote:
            html_nodes.append(quote_to_html_node(blocks[i]))
            
        elif block_types[i] == block_type_heading:
            html_nodes.append(heading_to_html_node(blocks[i]))
            
        elif block_types[i] == block_type_ordered_list:
            html_nodes.append(ordered_list_to_html_node(blocks[i]))
            
        elif block_types[i] == block_type_unordered_list:
            html_nodes.append(unordered_list__to_html_node(blocks[i]))
        
    return ParentNode(tag="div", children=html_nodes)