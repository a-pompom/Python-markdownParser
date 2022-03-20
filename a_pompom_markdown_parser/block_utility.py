from a_pompom_markdown_parser.element.block import Block


# 各モジュールから参照される、Block要素を加工したものを得るためのUtility
def get_text_from_block(block: Block) -> str:
    """
    Inline要素を子に含むBlock要素から、マークダウンの記法を除いたテキストを抽出

    :param block: 対象Block要素
    :return: Block要素が含むマークダウンの記法を除いた文字列
    """

    text = ''
    for child in block.children:
        if isinstance(child, Block):
            text += get_text_from_block(child)

        text += child.text

    return text
