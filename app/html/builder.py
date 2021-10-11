from app.element.block import Block, ParseResult
from app.element.inline import Inline
from app.html.block_builder import BlockBuilder
from app.html.inline_builder import InlineBuilder


class HtmlBuilder:
    """ マークダウンのパース結果からHTML文字列を組み立てることを責務に持つ """

    def __init__(self):
        self._block_builder = BlockBuilder()
        self._inline_builder = InlineBuilder()

    def build(self, parse_result: ParseResult) -> str:
        """
        パース結果をもとにHTML文字列を組み立て

        :param parse_result: マークダウンのパース結果
        :return: HTML文字列
        """

        html_text = ''

        for block in parse_result.content:
            html_text += self._build_block(block)

        return html_text

    def _build_block(self, block: Block) -> str:
        """
        BlockをもとにHTML文字列を組み立て

        :param block: 入力Block要素
        :return: HTML文字列
        """

        child_text = ''

        for child in block.children:

            # Inline
            if isinstance(child, Inline):
                child_text += self._inline_builder.build(child)
                continue

            # Block 再帰でHTML文字列を組み立て
            if isinstance(child, Block):
                child_text += self._build_block(child)
                continue

        # childrenの組み立て結果文字列とBlock要素の組み立て結果を組み合わせることで、
        # Block要素のHTML文字列への変換を実現
        return self._block_builder.build(block, child_text)
