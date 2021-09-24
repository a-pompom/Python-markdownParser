import re

from app.element.inline import Inline, PlainInline, LinkInline
from app.element.style import Plain, Link


class InlineParser:

    def __init__(self):
        # 各変換処理を表現する要素を初期化
        self.parsers: list[IParser] = [LinkParser()]

    def parse(self, text: str) -> list[Inline]:
        """
        マークダウンの文字列をもとに、Inline要素へ分割した結果を生成

        :param text: 対象文字列
        :return: Block要素が持つ子要素
        """

        children = []

        for parser in self.parsers:
            # Inline要素が存在したとき、ただInline要素を抜き出すだけでは元のテキストのどの部分が対応していたか判別できない
            # 順序関係を維持し、複数のInline要素にも対応できるよう、前後の文字列も抜き出す
            if parser.is_target(text):
                head, inline, tail = parser.parse(text)

                # 前方
                if head:
                    children.append(self.parse(head))

                # Inline
                children.append(inline)

                # 後方
                if tail:
                    children.append(self.parse(tail))

                return children

        return [PlainInline(Plain(), text)]


class IParser:
    """ マークダウンで書かれた行を解釈し、Inline要素を生成することを責務に持つ """

    def is_target(self, markdown_text: str) -> bool:
        """
        マークダウンの行が現在参照しているパーサの処理対象であるか判定
        たとえば、`[link](address)`の場合、LinkParserのみTrueを返し、それ以外はFalseを返す

        :param markdown_text: 判定対象行
        :return: パース対象 ->True パース対象でない -> False
        """
        raise NotImplementedError()

    def parse(self, markdown_text: str) -> tuple[str, Inline, str]:
        """
        マークダウンの行を解釈し、種類に応じたInline要素を生成 Inline要素と前後の文字列を返却\n
        たとえば、`this is [link](address) text`の場合、['this is', Inline, 'text']となる\n
        こうすることで、解釈結果と元のテキストで順序関係を保つことができる

        :param markdown_text: マークダウンの文字列
        :return 変換結果
        """
        raise NotImplementedError()


class LinkParser(IParser):
    """ リンク要素の解釈を責務に持つ """

    # ex) マークダウンの[Wikipedia](https://en.wikipedia.org/wiki/Markdown)へのリンクです
    PATTERN = r'(.*)\[(.*)\]\((.*)\)(.*)'

    def is_target(self, markdown_text: str) -> bool:
        return re.match(self.PATTERN, markdown_text) is not None

    def parse(self, markdown_text: str) -> tuple[str, Inline, str]:
        """
        リンクを表すInline要素を生成

        :param markdown_text: 処理対象文字列
        :return: リンクを表すInline要素
        """

        match: re.Match = re.match(self.PATTERN, markdown_text)
        # 遷移先URL・リンクテキストを属性として切り出し
        head_text, link_text, href, tail_text = (match.group(1), match.group(2), match.group(3), match.group(4))

        return head_text, LinkInline(Link(href=href), link_text), tail_text
