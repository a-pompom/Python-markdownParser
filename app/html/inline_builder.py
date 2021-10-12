from app.element.inline import Inline, LinkInline, CodeInline


class InlineBuilder:
    """ Inline要素と対応するHTML文字列を組み立てることを責務に持つ """

    def __init__(self):
        self._builders: list[IBuilder] = [LinkBuilder(), CodeBuilder()]

    def build(self, inline: Inline) -> str:
        """
        Inline要素と対応するHTMlタグを組み立て

        :param inline: 処理対象Inline要素
        :return: HTML文字列
        """

        for builder in self._builders:

            if builder.is_target(inline):
                return builder.build(inline)

        # Plain
        return inline.text


class IBuilder:
    """ Inline要素を解釈し、HTMLタグを表現する文字列を生成することを責務に持つ """

    def is_target(self, inline: Inline) -> bool:
        """
        Inline要素の種別がビルダと対応したものであるか判定

        :param inline: 判定対象Inline要素
        :return: ビルド対象-> True ビルド対象でない-> False
        """
        raise NotImplementedError

    def build(self, inline: Inline) -> str:
        """
        Inline要素をもとにHTML文字列を組み立て

        :param inline: 処理対象Inline要素
        :return: 組み立て結果のHTML文字列
        """
        raise NotImplementedError


class LinkBuilder(IBuilder):
    """ aタグで表されるリンク要素を生成することを責務に持つ """

    HREF_EXPRESSION = '{href}'
    TEXT_EXPRESSION = '{text}'
    TEMPLATE = f'<a href="{HREF_EXPRESSION}">{TEXT_EXPRESSION}</a>'

    def is_target(self, inline: Inline) -> bool:
        return isinstance(inline, LinkInline)

    def build(self, inline: LinkInline) -> str:
        """
        aタグHTML文字列を組み立て

        :param inline: 処理対象Inline要素
        :return: aタグHTML文字列
        """

        href = inline.style.href
        # <a href="url">text</a>
        anchor_tag = self.TEMPLATE.replace(
            self.HREF_EXPRESSION, href,
        ).replace(
            self.TEXT_EXPRESSION, inline.text
        )

        return anchor_tag


class CodeBuilder(IBuilder):
    """ codeタグで表現されるコード要素を生成することを責務に持つ """

    TEXT_EXPRESSION = '{text}'
    TEMPLATE = f'<code>{TEXT_EXPRESSION}</code>'

    def is_target(self, inline: Inline) -> bool:
        return isinstance(inline, CodeInline)

    def build(self, inline: CodeInline) -> str:
        """
        codeタグ文字列を組み立て

        :param inline: 処理対象Inline要素
        :return: codeタグ文字列
        """

        code_tag = self.TEMPLATE.replace(
            self.TEXT_EXPRESSION, inline.text
        )

        return code_tag
