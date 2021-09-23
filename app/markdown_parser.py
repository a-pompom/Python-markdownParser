from __future__ import annotations
from typing import Union
import dataclasses
import re

from app.element.style import Plain, Heading, Link
from app.element.block import Block, PlainBlock, HeadingBlock
from app.element.inline import Inline, PlainInline, LinkInline


@dataclasses.dataclass
class ParseResult:
    """ 変換結果を保持 """
    content: list[Block]


class MarkdownParser:
    """ マークダウン変換処理を責務に持つ """

    def __init__(self):
        # 各変換処理を表現する要素を初期化
        self.block_parsers: list[BlockParser] = [HeadingParser()]
        self.inline_parsers: list[InlineParser] = [LinkParser()]

    def parse(self, markdown_text: list[str]) -> ParseResult:
        """
        変換結果オブジェクトを生成

        :param markdown_text: 入力テキスト
        :return: ツリー構造による変換結果オブジェクト
        """

        result = []
        for line in markdown_text:
            inline_text = self._extract_inline_text(line)
            children = self._generate_inline_children(inline_text)

            block = self._generate_block(line, children)
            result.append(block)

        return ParseResult(result)

    def _extract_inline_text(self, markdown_text) -> str:
        """
        処理対象行からBlock要素の記法を除外したものを抽出

        :param markdown_text: 対象行文字列
        :return: 対象行文字列からBlock要素の記法を除いたもの
        """

        for block_parser in self.block_parsers:
            if block_parser.is_target(markdown_text):
                return block_parser.extract_text(markdown_text)

        return markdown_text

    def _generate_inline_children(self, text: str) -> list[Inline]:
        """
        マークダウンの文字列をもとに、Inline要素へ分割した結果を生成

        :param text: 対象文字列
        :return: Block要素が持つ子要素
        """

        children = []

        for parser in self.inline_parsers:
            # Inline要素が存在したとき、ただInline要素を抜き出すだけでは元のテキストのどの部分が対応していたか判別できない
            # 順序関係を維持し、複数のInline要素にも対応できるよう、前後の文字列も抜き出す
            if parser.is_target(text):
                head, inline, tail = parser.parse(text)

                # 前方
                if head:
                    children.append(self._generate_inline_children(head))

                # Inline
                children.append(inline)

                # 後方
                if tail:
                    children.append(self._generate_inline_children(tail))

                return children

        return [PlainInline(Plain(), text)]

    def _generate_block(self, line: str, children: list[Inline]) -> Block:
        """
        マークダウンパーサを介して行をBlock要素へ変換

        :param line: 処理対象行
        :param children: 子要素
        :return: 変換結果のBlock要素
        """

        for parser in self.block_parsers:
            if parser.is_target(line):
                return parser.parse(line, children)

        return PlainBlock(Plain(), children)


class BlockParser:
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

    def parse(self, markdown_text: str, children: list[Union[Inline, Block]]) -> Block:
        """
        マークダウンの行を解釈し、種類に応じたBlock要素を生成

        :param markdown_text: マークダウンの1行文字列
        :param children: Inlineパーサによって解釈された要素の集まり
        :return 変換結果
        """
        raise NotImplementedError()


class HeadingParser(BlockParser):
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

    def parse(self, markdown_text: str, children: list[Union[Inline, Block]]) -> Block:
        """
        ヘッダ行を解釈

        :param markdown_text: 処理対象行
        :param children: Inlineパーサによって解釈された要素の集まり
        :return: ヘッダを表すBlock要素
        """

        match: re.Match = re.match(self.PATTERN, markdown_text)
        heading_style, text = (match.group(1), match.group(2))

        return HeadingBlock(Heading(size=len(heading_style)), children)


class InlineParser:
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


class LinkParser(InlineParser):
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
