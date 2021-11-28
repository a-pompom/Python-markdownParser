from app.element.block import Block, HeadingBlock, QuoteBlock


class BlockBuilder:
    """ Block要素をもとに対応するHTML文字列を組み立てることを責務に持つ"""

    def __init__(self):
        self._builders: list[IBuilder] = [HeadingBuilder(), QuoteBuilder()]

    def build(self, block: Block, child_text: str) -> str:
        """
        Block要素をもとに対応するHTML文字列を生成

        :param block: 処理対象Block要素
        :param child_text: 子要素を解釈した結果の文字列
        :return: HTML文字列
        """

        for builder in self._builders:

            if builder.is_target(block):
                return builder.build(block, child_text)

        # Plain
        return child_text


class IBuilder:
    """ 各タグと対応するHTML要素の組み立てを責務に持つ """

    def is_target(self, block: Block) -> bool:
        """
        Block要素の種別がビルダと対応したものであるか判定

        :param block: 判定対象Block要素
        :return: ビルド対象-> True ビルド対象でない-> False
        """
        raise NotImplementedError

    def build(self, block: Block, child_text: str) -> str:
        """
        Block要素をもとにHTMLタグ要素を組み立て

        :param block: Block要素
        :param child_text: タグの子要素である文字列
        :return: HTML文字列
        """
        raise NotImplementedError


class HeadingBuilder(IBuilder):
    """ hタグ(ヘッダ)の組み立てを責務に持つ """

    HEADING_EXPRESSION = '{h}'
    TEXT_EXPRESSION = '{text}'
    TEMPLATE = f'<{HEADING_EXPRESSION}>{TEXT_EXPRESSION}</{HEADING_EXPRESSION}>'

    def is_target(self, block: Block) -> bool:
        return isinstance(block, HeadingBlock)

    def build(self, block: HeadingBlock, child_text: str) -> str:
        """
        ヘッダのHTML文字列を組み立て

        :param block: 組み立て元Block要素
        :param child_text: 子要素文字列
        :return: HTMLのヘッダタグを含む文字列
        """

        heading_size = f'h{block.style.size}'
        # <h~>text</h~> ※ ~はヘッダの大きさ
        heading = self.TEMPLATE.replace(
            self.HEADING_EXPRESSION, heading_size
        ).replace(
            self.TEXT_EXPRESSION, child_text
        )

        return heading


class QuoteBuilder(IBuilder):
    """ blockquote(引用)タグの組み立てを責務に持つ """

    TEXT_EXPRESSION = '{text}'
    TEMPLATE = f'<blockquote>{TEXT_EXPRESSION}</blockquote>'

    def is_target(self, block: Block) -> bool:
        return isinstance(block, QuoteBlock)

    def build(self, block: QuoteBlock, child_text: str) -> str:
        """
        引用要素のHTML文字列を組み立て

        :param block: 組み立て元Block要素
        :param child_text: 子要素文字列
        :return: HTMLのblockquoteタグを含む文字列
        """

        # <blockquote>text</blockquote>
        blockquote = self.TEMPLATE.replace(
            self.TEXT_EXPRESSION, child_text
        )

        return blockquote
