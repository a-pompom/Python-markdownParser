from app.regex import regex
from app.element.inline import Inline, PlainInline, LinkInline, CodeInline, ImageInline
from app.element.style import Plain, Link, Code, Image


class InlineParser:
    """ Inline要素と対応するマークダウンの記法を解釈することを責務に持つ """

    def __init__(self):
        # 各変換処理を表現する要素を初期化
        self.parsers: list[IParser] = [LinkParser(), CodeParser(), ImageParser()]

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
                head, inline_text, tail = parser.extract_text(text)
                inline = parser.parse(inline_text)

                # 前方
                if head:
                    children = [*children, *self.parse(head)]

                # Inline
                children.append(inline)

                # 後方
                if tail:
                    children = [*children, *self.parse(tail)]

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

    def extract_text(self, markdown_text: str) -> tuple[str, str, str]:
        """
        マークダウンの行を解釈し、Inline要素文字列と、前後の文字列を返却\n
        たとえば、`this is [link](address) text`の場合、['this is', '[link](address)', 'text']となる\n
        このように分離していくことで、解釈結果と元のテキストで順序関係を保つことができる

        :param markdown_text: 分離対象文字列
        :return: 先頭, Inline要素文字列, 末尾を格納したタプル
        """
        raise NotImplementedError()

    def parse(self, inline_text: str) -> Inline:
        """
        Inline要素の記法で書かれた文字列をもとに、Inline要素を生成\n
        分離処理と分けておくことで、テストコードで独立して扱うことができる

        :param inline_text: 解釈対象となるInline要素文字列
        :return 変換結果
        """
        raise NotImplementedError()


class LinkParser(IParser):
    """ リンク要素の解釈を責務に持つ """

    # imgタグの記法はリンク要素と共通しているため、除外するためのパターンを設定
    # ex) マークダウンの[Wikipedia](https://en.wikipedia.org/wiki/Markdown)へのリンクです
    PATTERN = r'\[(.*)\]\((.*)\)'
    EXTRACT_PATTERN = r'(.*)(?<!!)(\[.*\]\(.*\))(.*)'

    def is_target(self, markdown_text: str) -> bool:
        return regex.contain(self.EXTRACT_PATTERN, markdown_text)

    def extract_text(self, markdown_text: str) -> tuple[str, str, str]:
        head, inline, tail = regex.extract_from_group(self.EXTRACT_PATTERN, markdown_text, [1, 2, 3])
        return head, inline, tail

    def parse(self, markdown_text: str) -> LinkInline:
        """
        リンクを表すInline要素を生成

        :param markdown_text: 処理対象文字列
        :return: リンクを表すInline要素
        """

        # 遷移先URL・リンクテキストを属性として切り出し
        link_text, href = regex.extract_from_group(self.PATTERN, markdown_text, [1, 2])

        return LinkInline(Link(href=href), link_text)


class CodeParser(IParser):
    """ コード要素の解釈を責務に持つ """

    # ex) Pythonでは、コメントを`#`から始まる行で表現します
    PATTERN = r'`(.*)`'
    EXTRACT_PATTERN = r'(.*)(`.*`)(.*)'

    def is_target(self, markdown_text: str) -> bool:
        return regex.contain(self.EXTRACT_PATTERN, markdown_text)

    def extract_text(self, markdown_text: str) -> tuple[str, str, str]:
        head, inline, tail = regex.extract_from_group(self.EXTRACT_PATTERN, markdown_text, [1, 2, 3])
        return head, inline, tail

    def parse(self, markdown_text: str) -> CodeInline:
        """
        コードを表すInline要素を生成

        :param markdown_text: 処理対象文字列
        :return: コードを表すInline要素
        """

        code_text = regex.extract_from_group(self.PATTERN, markdown_text, [1])

        return CodeInline(Code(), code_text)


class ImageParser(IParser):
    """ 画像要素の解釈を責務に持つ """

    # ex) this ![amazing image](url) is awesome.
    PATTERN = r'!\[(.*)\]\((.*)\)'
    EXTRACT_PATTERN = r'(.*)(!\[.*\]\(.*\))(.*)'

    def is_target(self, markdown_text: str) -> bool:
        return regex.contain(self.EXTRACT_PATTERN, markdown_text)

    def extract_text(self, markdown_text: str) -> tuple[str, str, str]:
        head, inline, tail = regex.extract_from_group(self.EXTRACT_PATTERN, markdown_text, [1, 2, 3])
        return head, inline, tail

    def parse(self, markdown_text: str) -> ImageInline:
        """
        画像を表すInline要素を生成

        :param markdown_text: 処理対象文字列
        :return: 画像を表すInline要素
        """

        alt, src = regex.extract_from_group(self.PATTERN, markdown_text, [1, 2])

        # imgタグは子要素のテキストを持たない
        return ImageInline(Image(src=src, alt=alt), '')


# 特殊な要件に応じたInline要素の生成
def create_plain_inline(markdown_text: str) -> PlainInline:
    """
    パース処理なしで元のマークダウンの行と対応するInline要素を生成\n
    これは、コードブロックのような、元の記法をそのまま出力したい場合などで必要

    :param markdown_text: 元のマークダウンの行文字列
    :return: 元の文字列をそのまま格納したInline要素
    """
    return PlainInline(Plain(), markdown_text)
