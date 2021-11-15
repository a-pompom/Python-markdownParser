import dataclasses
from app.element.style import Style, Plain, Link, Code, Image


@dataclasses.dataclass
class Inline:
    """ aタグのようなインラインスタイルを保持 """
    style: Style
    text: str


@dataclasses.dataclass
class PlainInline(Inline):
    """ どの記法にも属さないInline要素 """
    style: Plain

    def __repr__(self):
        return f'Plain: text={self.text}'


@dataclasses.dataclass
class LinkInline(Inline):
    """ aタグと対応するリンク要素を保持 """
    style: Link

    def __repr__(self):
        return f'Link: text={self.text}, href={self.style.href}'


@dataclasses.dataclass
class CodeInline(Inline):
    """ codeタグと対応するコード要素を保持 """
    style: Code

    def __repr__(self):
        return f'Code: text={self.text}'


class ImageInline(Inline):
    """ imgタグと対応する画像要素を保持 """
    style: Image

    def __repr__(self):
        return f'Image: src={self.style.src}, alt={self.style.alt}'
