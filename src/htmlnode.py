class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method is not implemented")

    def props_to_html(self):
        if self.props == None:
            return ""
        
        attributes = ""
        for attribute in self.props:
            attributes += f' {attribute}="{self.props[attribute]}"'
        return attributes
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

# LeadNode-------------------------------------------------------------------------------    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Must have a value.")
        
        if self.tag == None:
            return self.value
        
        html = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return html
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"