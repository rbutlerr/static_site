
def markdown_to_blocks(markdown: str):
    block_chain = markdown.split('\n\n') #haha blockchain

    return [item.strip() for item in block_chain if item.strip()]