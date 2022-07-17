from a_pompom_markdown_parser.element.block import ParseResult, Block
from a_pompom_markdown_parser.markdown.block_parser import BlockParser
from a_pompom_markdown_parser.markdown.inline_parser import InlineParser
from a_pompom_markdown_parser.markdown.multi_line_parser import MultiLineParser


class MarkdownParser:
    """ マークダウン変換処理を責務に持つ """

    def __init__(self):
        self.block_parser = BlockParser()
        self.inline_parser = InlineParser()
        self.multi_line_parser = MultiLineParser()

    def parse(self, markdown_text: list[str]) -> ParseResult:
        """
        変換結果オブジェクトを生成

        :param markdown_text: 入力テキスト
        :return: ツリー構造による変換結果オブジェクト
        """

        result = []
        # 探索範囲を順々に狭めていくことで、単一の行・複数の行それぞれを対象としたマークダウンの記法を同質に解釈することができる
        while True:

            # テキストをすべて走査するまで
            if len(markdown_text) == 0:
                break

            # 単一行のみ解釈
            if not self.multi_line_parser.is_target(markdown_text[0]):
                result.append(self._create_block(markdown_text.pop(0)))
                continue

            # 複数行を解釈
            parsed, parse_range = MultiLineParser().parse(markdown_text)
            result = [*result, *parsed]
            del markdown_text[0:parse_range + 1]

        return ParseResult(result)

    def _create_block(self, line: str) -> Block:
        """
        1行のテキストからBlock要素を生成

        :param line: 1行のテキスト
        :return: パース処理により生成されたBlock要素
        """

        # 通常、変換後のHTML要素にはBlock要素の記法を含むべきではないので、
        # Inline要素は記法を除外したものを入力とする
        inline_text = self.block_parser.extract_inline_text(line)
        children = self.inline_parser.parse(inline_text)

        return self.block_parser.parse(line, children)
