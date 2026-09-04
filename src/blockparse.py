from enum import Enum
import re
class BlockType(Enum):
    paragraph = 1
    heading = 2
    code = 3
    quote = 4
    unordered_list = 5
    ordered_list = 6


def markdown_to_blocks(markdown: str):
    block_chain = markdown.split('\n\n') #haha blockchain

    return [item.strip() for item in block_chain if item.strip()]

def block_to_block_type(md_block: str):
    if re.fullmatch(r'^#{1,6}\s.*$',md_block):
        return BlockType.heading
    elif re.fullmatch(r'^```\n[\s\S]*```$',md_block):
        return BlockType.code
    elif re.fullmatch(r'^>.*$',md_block, flag=re.MULTILINE):
        return BlockType.quote
    elif re.fullmatch(r'^- .*$', md_block, flag=re.MULTILINE):
        return BlockType.unordered_list
    list_nums = re.findall(r'^([0-9][0-9]|[0-9])\. .*$', md_block, flag=re.MULTILINE)
    nums_ordered = True
        for i in range(len(list_nums)):
            if list_nums[i] != i + 1:
            nums_ordered = False


    elif re.fullmatch(r'^([0-9][0-9]|[0-9])\. .*$', md_block, flag = re.MULTILINE) and nums_ordered:
        return BlockType.ordered_list
    else:
        return BlockType.paragraph


