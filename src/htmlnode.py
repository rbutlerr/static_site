

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if (self.props is None or 
            self.props == {}):
            return ''
        html_props = ''
        for key, value in self.props.items():
            html_props += (f' {key}="{value}"')
        return html_props



    def __repr__(self):
        return f"""HTMLnode(
        tag = {self.tag or ""},
        value = {self.value or ""},
        children = {self.children or ""},
        props = {self.props or ""})
        """

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f"""HTMLnode(
        tag = {self.tag or ""},
        value = {self.value or ""},
        props = {self.props or ""})
        """

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag,None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Object lacks a tag")
        if self.children is None:
            raise ValueError("Object lacks children")
        child_html = ""
        for child in self.children:
            child_html += child.to_html()
        return f'<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>'
        

