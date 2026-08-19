import unittest
from textnode import (TextNode, TextType, text_node_to_html_node, 
                      split_nodes_delimiter, extract_markdown_images, extract_markdown_links, 
                      split_nodes_image, split_nodes_link,text_to_text_nodes)


class TextTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    

    def test_eq2(self):
        node = TextNode("a1",TextType.LINK,"https://lskjd.com")
        node2 = TextNode("a1",TextType.LINK,"https://lskjd.com")
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("a1",TextType.TEXT)
        node2 = TextNode("a2",TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq2(self):
        node = TextNode("a1", TextType.TEXT)
        node2 = TextNode("a1", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq3(self):
        node = TextNode("a1", TextType.LINK, "url1")
        node2 = TextNode("a1", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_convert(self):
        node = TextNode("text body", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "text body")
    
    def test_convert_2(self):
        node = TextNode("alt text", TextType.IMAGE, "www.image.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src":"www.image.com",
                                           "alt":"alt text"})
        self.assertEqual(html_node.children, None)

    def test_split_nodes(self):
        node = TextNode("this **bold** text",TextType.TEXT)
        split_1 = TextNode("this ",TextType.TEXT)
        split_2 = TextNode("bold",TextType.BOLD)
        split_3 = TextNode(" text",TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node],"**",TextType.TEXT),[split_1, split_2, split_3])

    def test_split_nodes_invalid(self):
        node = TextNode("this **invalid text", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node],"**",TextType.TEXT)

    def test_split_nodes_invalid_delim(self):
        node = TextNode("text", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node],"*",TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node],"`",TextType.TEXT),[node])
    def test_split_nodes_multisplit(self):
        node = TextNode("**multi**`split`_node_**multi**`split`_node_",TextType.TEXT)
        node2 = TextNode("node2 is **bold** only",TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node,node2],"**",TextType.TEXT),[
            TextNode("multi",TextType.BOLD),
            TextNode("`split`_node_", TextType.TEXT),
            TextNode("multi",TextType.BOLD),
            TextNode("`split`_node_",TextType.TEXT),
            TextNode("node2 is ",TextType.TEXT),
            TextNode("bold",TextType.BOLD),
            TextNode(" only", TextType.TEXT)
            ])
        self.assertEqual(split_nodes_delimiter([node, node2],"_",TextType.TEXT),[
            TextNode("**multi**`split`",TextType.TEXT),
            TextNode("node", TextType.ITALIC),
            TextNode("**multi**`split`",TextType.TEXT),
            TextNode("node",TextType.ITALIC),
            node2
            ])

    def test_img_link_extract(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)" 
        self.assertEqual(extract_markdown_images(text),
        [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
        text_2 = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text_2),
                         [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
        self.assertEqual(extract_markdown_images(text_2),
                         [])
        self.assertEqual(extract_markdown_links(text),
                         [])
        matches = extract_markdown_images(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
            )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    def test_split_images_duplicate(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )
    def test_split_links(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ], new_nodes
        )
    def test_text_textnodes(self):
        self.assertListEqual(
            [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ],
        text_to_text_nodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        )

if __name__ == "__main__":
    unittest.main()
