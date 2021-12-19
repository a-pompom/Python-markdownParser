import dataclasses


@dataclasses.dataclass
class Inline:
    """ aタグのようなインラインスタイルを保持 """
    text: str


@dataclasses.dataclass
class PlainInline(Inline):
    """ どの記法にも属さないInline要素 """

    def __repr__(self):
        return f'Plain: text={self.text}'


@dataclasses.dataclass
class LinkInline(Inline):
    """ aタグと対応するリンク要素を保持 """
    href: str

    def __repr__(self):
        return f'Link: text={self.text}, href={self.href}'


@dataclasses.dataclass
class CodeInline(Inline):
    """ codeタグと対応するコード要素を保持 """

    def __repr__(self):
        return f'Code: text={self.text}'


@dataclasses.dataclass
class ImageInline(Inline):
    """ imgタグと対応する画像要素を保持 """
    src: str
    alt: str

    def __repr__(self):
        return f'Image: src={self.src}, alt={self.alt}'


@dataclasses.dataclass
class HorizontalRuleInline(Inline):
    """ hrタグと対応する水平罫線要素を保持 """

    def __repr__(self):
        return f'HorizontalRule: '
