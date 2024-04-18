class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props:
            converted = ""
            for k, v in self.props.items():
                converted += f" {k}=\"{v}\""
            return converted
                
        
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):

        if self.tag is None:
            return self.value
        
        if self.value is None:
            raise ValueError("Leaf nodes need a value")
                
        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("A parent node requires a tag")
        if self.children is None:
            raise ValueError("A parent node requires children")
        
        result = f"<{self.tag}>"
        if self.children:
            for child in self.children:
                result += child.to_html()
        result += f"</{self.tag}>"
        return result