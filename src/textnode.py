from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
    TEXT = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url
    def __eq__(self, other):
        return (self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url)
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    try:
        node_type = TextType(text_node.text_type)
    except ValueError:
        print(f"Error: invalid text type: {text_node.text_type}")

    tag = None
    value = None
    props = None
    
    if node_type == TextType.TEXT:
        value = text_node.text
    elif node_type == TextType.BOLD:
        tag = "b"
        value = text_node.text
    elif node_type == TextType.ITALIC:
        tag = "i"
        value = text_node.text
    elif node_type == TextType.CODE:
        tag = "code"
        value = text_node.text
    elif node_type == TextType.LINK:
        tag = "a"
        value = text_node.text
        props = {"href":text_node.url}
    elif node_type == TextType.IMAGE:
        tag = "img"
        props = {
                "src":text_node.url,
                "alt":text_node.text
                }
    return LeafNode(tag, value, props)

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    ##This is a very dumb function
    ##do not try to input crazy stuff, just inline unnested formatting
    delim_text_type_map = {
            "**":text_type.BOLD,
            "_":text_type.ITALIC,
            "`":text_type.CODE}
    if delimiter not in delim_text_type_map:
        raise ValueError(f"invalid delimiter: {delimiter}")
    split_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_nodes.append(node)

        split = node.text.split(delimiter)
        if len(split)%2 == 0:
            raise Exception(f"invalid markdown: {node.text} is missing closing delimiter")
        for i in range(len(split)):
            if split[i] == "":
                continue
            if i%2 == 1:
                split_nodes.append(TextNode(split[i],delim_text_type_map[delimiter]))
            else:
                split_nodes.append(TextNode(split[i],TextType.TEXT))


    return split_nodes

def extract_markdown_images(text: str) -> list:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)",text)
    return matches

def extract_markdown_links(text:str) -> list:
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches

        

