from app.markdown.parser import ParseResult
from app.element.block import Block, PlainBlock, HeadingBlock


class HtmlBuilder:
    """ HTML文字列の生成を責務に持つ """

    def __init__(self):
        self.builders = [HeadingBuilder()]

    def build(self, html_input: ParseResult) -> str:
        """
        入力をもとにHTML文字列を組み立て

        :param html_input: 入力要素 Block/Inlineからなるツリー要素
        :return: HTML文字列
        """

        html = []

        for block in html_input.content:

            for builder in self.builders:

                line: str = (
                    (isinstance(block, HeadingBlock) and builder.build(block)) or
                    (isinstance(block, PlainBlock) and self._get_plain_text(block))
                )
                html.append(line)

        return ''.join(html)

    def _get_plain_text(self, block: PlainBlock) -> str:
        return block.children[0].text


class Builder:
    """ 各タグと対応するHTML要素の組み立てを責務に持つ """

    def build(self, block: Block) -> str:
        raise NotImplementedError


class HeadingBuilder(Builder):
    """ hタグ(ヘッダ)の組み立てを責務に持つ """

    def build(self, block: HeadingBlock) -> str:
        """
        ヘッダのHTML文字列を組み立て

        :param block: 組み立て元Block要素
        :return: HTMLのヘッダタグを含む文字列
        """

        text = ''
        for child in block.children:
            if isinstance(child, str):
                text = child

        # <h1>text</h1>のような文字列を生成
        heading_expression = f'h{block.style.size}'
        return f'<{heading_expression}>{text}</{heading_expression}>'
