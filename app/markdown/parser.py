import dataclasses

from app.element.block import Block
from app.markdown.block_parser import BlockParser
from app.markdown.inline_parser import InlineParser


@dataclasses.dataclass
class ParseResult:
    """ 変換結果を保持 """
    content: list[Block]


class MarkdownParser:
    """ マークダウン変換処理を責務に持つ """

    def __init__(self):
        self.block_parser = BlockParser()
        self.inline_parser = InlineParser()

    def parse(self, markdown_text: list[str]) -> ParseResult:
        """
        変換結果オブジェクトを生成

        :param markdown_text: 入力テキスト
        :return: ツリー構造による変換結果オブジェクト
        """

        result = []
        for line in markdown_text:
            inline_text = self.block_parser.extract_inline_text(line)
            children = self.inline_parser.parse(inline_text)

            block = self.block_parser.parse(line, children)
            result.append(block)

        return ParseResult(result)
