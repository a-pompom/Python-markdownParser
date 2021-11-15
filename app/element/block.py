import dataclasses
from functools import reduce
from typing import Union

from app.element.style import Style, Plain, Heading
from app.element.inline import Inline

Children = list[Union[Inline, 'Block']]


def create_repr_children(block_name: str, children: Children) -> str:
    """
    子要素のrepr表現を生成

    :param block_name: Block要素名 どの要素の子か識別するために参照
    :param children: 生成対象
    :return: 子要素を文字列化したもの 子同士の区切りには`|`を使用
    """

    repr_children = ['']

    for child in children:
        # Inlineはそのまま子要素として追加
        if isinstance(child, Inline):
            repr_children.append(f'Child of {block_name} -> {repr(child)}')
            continue

        # Block要素はBlockをreprで評価した結果が子要素となる
        if isinstance(child, Block):
            repr_children += repr(child)

    return ' | '.join(repr_children)


@dataclasses.dataclass
class Block:
    """ 行要素を保持 """
    style: Style
    children: Children


@dataclasses.dataclass
class ParseResult:
    """ 変換結果を保持 """
    content: list[Block]

    def __repr__(self):
        return ' '.join([repr(block) for block in self.content])


@dataclasses.dataclass
class PlainBlock(Block):
    """ どの記法にも属さない要素 """
    style: Plain

    def __repr__(self):
        child_repr_text = create_repr_children('Plain', self.children)
        return f'[Plain:{child_repr_text}]'


@dataclasses.dataclass
class HeadingBlock(Block):
    """ ヘッダ要素 """
    style: Heading

    def __repr__(self):
        child_repr_text = create_repr_children('Heading', self.children)
        return f'[Heading: size={self.style.size}{child_repr_text}]'
