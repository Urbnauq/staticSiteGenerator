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
    
# ParentNode------------------------------------------------------------------------------- 
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Tag is required.")
        
        if self.children == None:
            raise ValueError("Children is required")
        
        child_html = ""
        for child in self.children:
            child_html += child.to_html()
        
        html = f'<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>'
        return html
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

        