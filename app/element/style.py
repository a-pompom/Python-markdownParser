import dataclasses


class Style:
    """ マークダウン・HTMLの記法の種類を表現 """


class Plain(Style):
    """ 修飾のないことを表現 """


@dataclasses.dataclass
class Heading(Style):
    """ ヘッダ要素を表現 """
    # h1, h3のようなヘッダの大きさを表現
    size: int


@dataclasses.dataclass
class Link(Style):
    """ リンク要素を表現 """
    href: str


@dataclasses.dataclass
class Code(Style):
    """ コード要素を表現 """
