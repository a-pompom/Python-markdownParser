import dataclasses
from typing import Union

from app.element.style import Style, Plain, Heading
from app.element.inline import Inline


@dataclasses.dataclass
class Block:
    """ 行要素を保持 """
    style: Style
    children: list[Union[Inline, 'Block']]


@dataclasses.dataclass
class PlainBlock(Block):
    """ どの記法にも属さない要素 """
    style: Plain


@dataclasses.dataclass
class HeadingBlock(Block):
    """ ヘッダ要素 """
    style: Heading
