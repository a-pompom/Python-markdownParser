import dataclasses
from typing import Union

from app.element.style import Style, Plain, Heading
from app.element.inline import Inline

Children = list[Union[Inline, 'Block']]


@dataclasses.dataclass
class Block:
    """ 行要素を保持 """
    style: Style
    children: Children


@dataclasses.dataclass
class ParseResult:
    """ 変換結果を保持 """
    content: list[Block]


@dataclasses.dataclass
class PlainBlock(Block):
    """ どの記法にも属さない要素 """
    style: Plain


@dataclasses.dataclass
class HeadingBlock(Block):
    """ ヘッダ要素 """
    style: Heading
