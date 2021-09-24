import re

from app.element.style import Plain, Heading
from app.element.block import Children, Block, PlainBlock, HeadingBlock


class BlockParser:

    def __init__(self):
        self.parsers: list[IParser] = [HeadingParser()]

    def extract_inline_text(self, markdown_text) -> str:
        """
        処理対象行からBlock要素の記法を除外したものを抽出

        :param markdown_text: 対象行文字列
        :return: 対象行文字列からBlock要素の記法を除いたもの
        """

        for block_parser in self.parsers:
            if block_parser.is_target(markdown_text):
                return block_parser.extract_text(markdown_text)

        return markdown_text

    def parse(self, line: str, children: Children) -> Block:
        """
        マークダウンパーサを介して行をBlock要素へ変換

        :param line: 処理対象行
        :param children: 子要素
        :return: 変換結果のBlock要素
        """

        for parser in self.parsers:
            if parser.is_target(line):
                return parser.parse(line, children)

        return PlainBlock(Plain(), children)


class IParser:
    """ マークダウンで書かれた行を解釈し、Block要素を生成することを責務に持つ """

    def is_target(self, markdown_text: str) -> bool:
        """
        マークダウンの行が現在参照しているパーサの処理対象であるか判定
        たとえば、`# Heading`の場合、HeadingParserのみTrueを返し、それ以外はFalseを返す

        :param markdown_text: 判定対象行
        :return: パース対象 ->True パース対象でない -> False
        """
        raise NotImplementedError()

    def extract_text(self, markdown_text: str) -> str:
        """
        Inline要素を組み立てるとき、Block要素の記法が関与しないよう切り出し
        これにより、Inline要素・Block要素それぞれのパース処理は、互いに関与せず、疎結合を保つことができる

        :param markdown_text: 対象行文字列
        :return: 対象行文字列からBlock要素の記法を抜いたもの
        """
        raise NotImplementedError()

    def parse(self, markdown_text: str, children: Children) -> Block:
        """
        マークダウンの行を解釈し、種類に応じたBlock要素を生成

        :param markdown_text: マークダウンの1行文字列
        :param children: Inlineパーサによって解釈された要素の集まり
        :return 変換結果
        """
        raise NotImplementedError()


class HeadingParser(IParser):
    """ ヘッダの解釈を責務に持つ"""
    PATTERN = '^(#+) (.*)'

    def __init__(self):
        pass

    def is_target(self, markdown_text: str) -> bool:
        return re.match(self.PATTERN, markdown_text) is not None

    def extract_text(self, markdown_text: str) -> str:
        match: re.Match = re.match(self.PATTERN, markdown_text)
        _, text = (match.group(1), match.group(2))

        return text

    def parse(self, markdown_text: str, children: Children) -> Block:
        """
        ヘッダ行を解釈

        :param markdown_text: 処理対象行
        :param children: Inlineパーサによって解釈された要素の集まり
        :return: ヘッダを表すBlock要素
        """

        match: re.Match = re.match(self.PATTERN, markdown_text)
        heading_style, text = (match.group(1), match.group(2))

        return HeadingBlock(Heading(size=len(heading_style)), children)
