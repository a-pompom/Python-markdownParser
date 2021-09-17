from __future__ import annotations
from typing import Union
import dataclasses


@dataclasses.dataclass
class Inline:
    """ aタグのようなインラインスタイルを保持 """
    style: str
    text: str


@dataclasses.dataclass
class Block:
    """ 行要素を保持 """
    style: str
    children: list[Union['Block', Inline, str]]


@dataclasses.dataclass
class ParseResult:
    """ 変換結果を保持 """
    content: list[Block]


class MarkdownParser:
    """ マークダウン変換処理を責務に持つ """

    def __init__(self):
        # 各変換処理を表現する要素を初期化
        self.parsers: list[Parser] = [HeadingParser()]

    def parse(self, markdown_text: list[str]) -> ParseResult:
        """
        変換結果オブジェクトを生成

        :param markdown_text: 入力テキスト
        :return: ツリー構造による変換結果オブジェクト
        """

        # TODO ParserでBlockオブジェクトをつくりたい
        result = []
        for line in markdown_text:
            result.append(Block('', [line]))

        return ParseResult(result)


class Parser:
    """ マークダウンで書かれた行の解釈を責務に持つ """
    def parse(self, markdown_text: str) -> Block:
        """
        マークダウンの行を解釈し、種類に応じてBlock/Inlineを生成

        :param markdown_text: マークダウンの1行文字列
        :return: 変換結果のBlock要素
        """
        raise NotImplementedError()


class HeadingParser(Parser):
    """ ヘッダの解釈を責務に持つ"""

    def __init__(self):
        pass

    def parse(self, markdown_text: str) -> Block:
        # TODO 変換処理実装
        pass
