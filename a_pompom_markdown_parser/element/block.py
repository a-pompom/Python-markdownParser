import dataclasses
from typing import Union

from a_pompom_markdown_parser.element.inline import Inline

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
        repr_children.append(f'Child of {block_name} -> {repr(child)}')

    return ' | '.join(repr_children)


def is_same_children(former: Children, latter: Children) -> bool:
    """
    2つのBlock要素の子が同一か比較

    :param former: 一方のBlock要素の子
    :param latter: もう一方のBlock要素の子
    :return: 子が同一 -> True, 異なる -> False
    """
    if len(former) != len(latter):
        return False

    # 子が双方空の場合は等価とみなす
    if len(former) == 0 and len(latter) == 0:
        return True

    for former_child, latter_child in zip(former, latter):
        if not former_child.__eq__(latter_child):
            return False

    return True


@dataclasses.dataclass
class Block:
    """ 行要素を保持 """
    children: Children

    def is_same_type(self, another: 'Block') -> bool:
        """
        2つのBlockが同種のものか判定

        :param another: 比較対象
        :return: 同種 -> True, 異種 -> False
        """
        return isinstance(self, type(another))

    def __eq__(self, other):
        raise NotImplementedError()


@dataclasses.dataclass
class ParseResult:
    """ 変換結果を保持 """
    content: list[Block]

    def __repr__(self):
        return ' '.join([repr(block) for block in self.content])

    def __eq__(self, other: 'ParseResult'):
        for self_block, other_block in zip(self.content, other.content):
            if not self_block.__eq__(other_block):
                return False

        return True


@dataclasses.dataclass
class PlainBlock(Block):
    """ どのHTMLタグにも変換されない要素 コードブロックで記述される """
    indent_depth: int = 0

    def __repr__(self):
        child_repr_text = create_repr_children('Plain', self.children)
        return f'[Plain: indent_depth={self.indent_depth}{child_repr_text}]'

    def __eq__(self, other: 'PlainBlock'):
        if self.indent_depth != other.indent_depth:
            return False

        return is_same_children(self.children, other.children)


@dataclasses.dataclass
class ParagraphBlock(Block):
    """ 段落要素 """
    indent_depth: int = 0

    def __repr__(self):
        child_repr_text = create_repr_children('Paragraph', self.children)
        return f'[Paragraph: indent_depth={self.indent_depth}{child_repr_text}]'

    def __eq__(self, other: 'ParagraphBlock'):
        if self.indent_depth != other.indent_depth:
            return False

        return is_same_children(self.children, other.children)


@dataclasses.dataclass
class HeadingBlock(Block):
    """ ヘッダ要素 """
    size: int

    def __repr__(self):
        child_repr_text = create_repr_children('Heading', self.children)
        return f'[Heading: size={self.size}{child_repr_text}]'

    def __eq__(self, other: 'HeadingBlock'):
        if self.size != other.size:
            return False

        return is_same_children(self.children, other.children)


@dataclasses.dataclass
class QuoteBlock(Block):
    """ 引用要素 """

    def __repr__(self):
        child_repr_text = create_repr_children('Quote', self.children)
        return f'[Quote:{child_repr_text}]'

    def __eq__(self, other: 'QuoteBlock'):
        return is_same_children(self.children, other.children)


@dataclasses.dataclass
class ListBlock(Block):
    """ リスト要素 """
    indent_depth: int = 0

    def __repr__(self):
        child_repr_text = create_repr_children('List', self.children)
        return f'[List: indent_depth={self.indent_depth}{child_repr_text}]'

    def __eq__(self, other: 'ListBlock'):
        if self.indent_depth != other.indent_depth:
            return False

        return is_same_children(self.children, other.children)


@dataclasses.dataclass
class ListItemBlock(Block):
    """ リスト子要素 """
    # リスト親要素の階層で描画されることから、必ず階層は1つ下より深くなる
    indent_depth: int = 1

    def __repr__(self):
        child_repr_text = create_repr_children('ListItem', self.children)
        return f'[ListItem: indent_depth={self.indent_depth}{child_repr_text}]'

    def __eq__(self, other: 'ListItemBlock'):
        if self.indent_depth != other.indent_depth:
            return False

        return is_same_children(self.children, other.children)


@dataclasses.dataclass
class ICodeBlock(Block):
    """ コードブロックを統合するためのインタフェース表現 """

    # コードブロックはICodeBlock型であれば同種とみなす
    # こうすることで、Converterにて、コード・子要素を同質に扱うことができる
    def is_same_type(self, another: 'Block') -> bool:
        return isinstance(another, ICodeBlock)

    def __eq__(self, other):
        raise NotImplementedError()


@dataclasses.dataclass
class CodeBlock(ICodeBlock):
    """ コードブロック要素 """
    language: str

    def __repr__(self):
        child_repr_text = create_repr_children('CodeBlock', self.children)
        return f'[CodeBlock: language={self.language}{child_repr_text}]'

    def __eq__(self, other: 'CodeBlock'):
        if self.language != other.language:
            return False

        return is_same_children(self.children, other.children)


@dataclasses.dataclass
class CodeChildBlock(ICodeBlock):
    """ コードブロック内部の要素 """

    def __repr__(self):
        child_repr_text = create_repr_children('CodeChildBlock', self.children)
        return f'[CodeChildBlock:{child_repr_text}]'

    def __eq__(self, other: 'CodeChildBlock'):
        return is_same_children(self.children, other.children)


@dataclasses.dataclass
class HorizontalRuleBlock(Block):
    """ hrタグと対応する水平罫線要素を保持 """

    def __repr__(self):
        child_repr_text = create_repr_children('HorizontalRule', self.children)
        return f'[HorizontalRule:{child_repr_text}]'

    def __eq__(self, other: 'HorizontalRuleBlock'):
        return is_same_children(self.children, other.children)
