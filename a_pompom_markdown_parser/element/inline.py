import dataclasses


@dataclasses.dataclass
class Inline:
    """ aタグのようなインラインスタイルを保持 """
    text: str

    def __eq__(self, other):
        raise NotImplementedError()


@dataclasses.dataclass
class PlainInline(Inline):
    """ どの記法にも属さないInline要素 """

    def __repr__(self):
        return f'Plain: text={self.text}'

    def __eq__(self, other: 'PlainInline'):
        return self.text == other.text


@dataclasses.dataclass
class LinkInline(Inline):
    """ aタグと対応するリンク要素を保持 """
    href: str

    def __repr__(self):
        return f'Link: text={self.text}, href={self.href}'

    def __eq__(self, other: 'LinkInline'):
        return self.href == other.href and self.text == other.text


@dataclasses.dataclass
class CodeInline(Inline):
    """ codeタグと対応するコード要素を保持 """

    def __repr__(self):
        return f'Code: text={self.text}'

    def __eq__(self, other: 'CodeInline'):
        return self.text == other.text


@dataclasses.dataclass
class ImageInline(Inline):
    """ imgタグと対応する画像要素を保持 """
    src: str
    alt: str

    def __repr__(self):
        return f'Image: src={self.src}, alt={self.alt}'

    def __eq__(self, other: 'ImageInline'):
        return self.src == other.src and self.alt == other.alt
