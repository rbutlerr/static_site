import unittest
from blockparse import markdown_to_blocks, block_to_block_type, BlockType

class TestBlockParse(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md) 
        self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )
    
    def test_markdown_to_blocks_crazy_lines(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line     

         
- This is a list
- with items
"""
        blocks = markdown_to_blocks(md) 
        self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )

    def test_markdown_to_blocks_single_line(self):
        md = "this just a line"
        self.assertEqual(
            markdown_to_blocks(md),
            ["this just a line"]
        )

    def test_block_type_check(self):
        self.assertEqual(
            BlockType.paragraph,
            block_to_block_type("skfjla")

        )
        self.assertEqual(
            BlockType.heading,
            block_to_block_type("124 headings")
            
        )
        self.assertEqual(
            BlockType.code,
            block_to_block_type("""```
            code block text you know
            this is still a code block
            > ohkk
            21 sldkf
            ```""")

        )

        quote = """> quote block
>these are quote
>still a quote"""
        self.assertEqual(
            BlockType.quote,
            block_to_block_type(quote)
            
        )
        self.assertEqual(
            BlockType.unordered_list,
            block_to_block_type(
                """- list item,
- next list item,
- another list item"""
            )
        )
        self.assertEqual(
            BlockType.ordered_list,
            block_to_block_type(
                """1. numberone
2. number two"""
            )
        )
        self.assertNotEqual(
            BlockType.ordered_list,
            block_to_block_type(
                """2. numbertwo,
3. out of order"""
            )
        )
        


