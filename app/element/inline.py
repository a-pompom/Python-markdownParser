import dataclasses
from app.element.style import Style, Plain, Link, Code


@dataclasses.dataclass
class Inline:
    """ aタグのようなインラインスタイルを保持 """
    style: Style
    text: str


@dataclasses.dataclass
class PlainInline(Inline):
    """ どの記法にも属さないInline要素 """
    style: Plain


@dataclasses.dataclass
class LinkInline(Inline):
    """ aタグと対応するリンク要素を保持 """
    style: Link


@dataclasses.dataclass
class CodeInline(Inline):
    """ codeタグと対応するコード要素を保持 """
    style: Code

