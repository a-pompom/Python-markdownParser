from app.element.block import Block, PlainBlock, HeadingBlock, Children
from app.element.inline import Inline, PlainInline, LinkInline
from app.element.style import Plain, Heading, Link


def create_block(block_type: str, children: Children, **kwargs) -> Block:
    """
    パラメータをもとにBlock要素を生成

    :param block_type: Blockの種類
    :param children: 子Inline要素
    :param kwargs: ヘッダの大きさなど、Block要素の付加属性
    :return: 生成されたBlock要素
    """

    if block_type == 'heading':
        return HeadingBlock(Heading(size=kwargs['size']), children)

    if block_type == '':
        return PlainBlock(Plain(), children)

    raise Exception('invalid block type')


def create_inline(inline_type: str, text: str, **kwargs) -> Inline:
    """
    パラメータをもとにInline要素を生成

    :param inline_type: Inlineの種類
    :param text: 格納文字列
    :param kwargs: リンクの参照など、Inline要素の付加属性
    :return: 生成されたInline要素
    """

    if inline_type == 'link':
        return LinkInline(Link(href=kwargs['href']), text)

    return PlainInline(Plain(), text)
