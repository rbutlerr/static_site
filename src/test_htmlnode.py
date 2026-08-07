import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_gen(self):
        node = HTMLNode("p","this is a paragraph of text")
        self.assertEqual(repr(node),
            """HTMLnode(
        tag = p,
        value = this is a paragraph of text,
        children = ,
        props = )
        """)
    def test_gen_2(self):

        node2_props = {
                "href": "https://www.google.com"}
        node2 = HTMLNode("a","link_me_please",None,node2_props)
        self.assertEqual(node2.props_to_html(),
            ' href="https://www.google.com"')
class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_to_html_(self):
        node = LeafNode("h1", "Big Heading")
        self.assertEqual(node.to_html(), "<h1>Big Heading</h1>")

    def test_leaf_to_html_img(self):
        
        node2_props = {
                "href": "https://www.google.com"}
        node2 = LeafNode("a","link_me_please",node2_props)
        self.assertEqual(node2.to_html(),
            '<a href="https://www.google.com">link_me_please</a>')
class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_big(self):
        node = ParentNode("div",
                [
                    LeafNode("b", "bold"),
                    ParentNode("ol", [
                        LeafNode("li", "list_1", {"href": "www.com"}),
                        LeafNode("li", "list_2"),
                        LeafNode("li", "list_3")
                        ]),
                    ParentNode("p", [
                        LeafNode("code","some_code"),
                        LeafNode("blockquote","some_quote")
                        ]),
                    ParentNode("b", [
                        ParentNode("i", [
                            LeafNode("p","bip")]
                        )]
                    )
                ])
        self.assertEqual(node.to_html(),
                         '<div><b>bold</b><ol><li href="www.com">list_1</li><li>list_2</li><li>list_3</li></ol><p><code>some_code</code><blockquote>some_quote</blockquote></p><b><i><p>bip</p></i></b></div>')

    def test_to_html_empties(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(),
                         '<div></div>')
    def test_to_html_err(self):
        with self.assertRaises(ValueError):
            ParentNode(None,[]).to_html()
        with self.assertRaises(ValueError):
            ParentNode("a", None).to_html()



                    


if __name__ == "__main__":
    unittest.main()
