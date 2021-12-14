from typing import Literal

from app.element.block import ParseResult, Block, CodeBlock
from app.markdown.block_parser import BlockParser, create_plain_block
from app.markdown.inline_parser import InlineParser, create_plain_inline


class ParseMode:
    """ 以前にパースした行に応じた変換方法を表現することを責務に持つ """

    def __init__(self):
        # 変換方法
        # コードブロックの場合は、内部ではパースしない
        self.current: Literal['Block'] | Literal['CodeBlock'] = 'Block'

    def is_code_block_mode(self, block: Block):
        """
        コードブロック内の要素としてパースすべきか判定

        :param block: 対象Block 一度パースしなければ種別は判別できないので、Block要素を入力とする
        :return: コードブロックの範囲内->True 範囲外->False
        """
        return self.current == 'CodeBlock' and not isinstance(block, CodeBlock)

    def update(self, block: Block):
        """
        変換モードを前後の行に応じて更新

        :param block: 現在行のBlock要素
        """

        # コードブロック終了
        if self.current == 'CodeBlock' and isinstance(block, CodeBlock):
            self.current = 'Block'
            return

        # コードブロック開始
        if isinstance(block, CodeBlock):
            self.current = 'CodeBlock'
            return


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
        parse_mode = ParseMode()

        for line in markdown_text:
            block = self._create_block_by_parse_mode(line, parse_mode)
            result.append(block)
            parse_mode.update(block)

        return ParseResult(result)

    def _create_block_by_parse_mode(self, line: str, parse_mode: ParseMode) -> Block:
        """
        変換モードに応じて、1行のテキストからBlock要素を生成

        :param line: 1行のテキスト
        :param parse_mode: 変換方法を表現したオブジェクト
        :return: パース処理により生成されたBlock要素
        """

        # 通常、変換後のHTML要素にはBlock要素の記法を含むべきではないので、
        # Inline要素は記法を除外したものを入力とする
        inline_text = self.block_parser.extract_inline_text(line)
        children = self.inline_parser.parse(inline_text)

        block = self.block_parser.parse(line, children)

        # コードブロックの中では、どのようなマークダウンの記法も解釈せず、そのまま出力
        if parse_mode.is_code_block_mode(block):
            return create_plain_block([create_plain_inline(line)])

        return block
