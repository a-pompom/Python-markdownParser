from app.element.block import Block, PlainBlock, ParagraphBlock, HeadingBlock, QuoteBlock, ListBlock, ListItemBlock, \
    CodeBlock, HorizontalRuleBlock

from app.settings import setting

# 全体で参照する設定値
LINE_BREAK = setting['newline_code']
INDENT = setting['indent']


def get_indent_text_from_depth(depth: int):
    """
    インデント文字列を階層の深さから取得

    :param depth: インデント階層の深さ
    :return: インデントを表現する文字列
    """
    return ''.join([INDENT for _ in range(depth)])


class BlockBuilder:
    """ Block要素をもとに対応するHTML文字列を組み立てることを責務に持つ"""

    def __init__(self):
        self._builders: list[IBuilder] = [ParagraphBuilder(), HeadingBuilder(), QuoteBuilder(), ListItemBuilder(),
                                          ListBuilder(), CodeBlockBuilder(), HorizontalRuleBuilder()]

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
        if isinstance(block, PlainBlock):
            return get_indent_text_from_depth(block.indent_depth) + child_text


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


class ParagraphBuilder(IBuilder):
    """ pタグ(段落)の組み立てを責務に持つ """

    INDENT_EXPRESSION = '{indent}'
    CLASSNAME_EXPRESSION = '{classname}'
    TEXT_EXPRESSION = '{text}'
    # example
    # <p class="...">
    #     これから説明します。
    # </p>
    TEMPLATE = (
        f'{INDENT_EXPRESSION}<p class="{CLASSNAME_EXPRESSION}">{LINE_BREAK}'
        f'{INDENT_EXPRESSION}{INDENT}{TEXT_EXPRESSION}{LINE_BREAK}'
        f'{INDENT_EXPRESSION}</p>'
    )

    def is_target(self, block: Block) -> bool:
        return isinstance(block, ParagraphBlock)

    def build(self, block: ParagraphBlock, child_text: str) -> str:
        """
        段落要素のHTML文字列を組み立て

        :param block: 組み立て元Block要素
        :param child_text: 子要素文字列
        :return: HTMLのpタグを含む文字列
        """

        paragraph = self.TEMPLATE.replace(
            self.INDENT_EXPRESSION, get_indent_text_from_depth(block.indent_depth)
        ).replace(
            self.CLASSNAME_EXPRESSION, setting['class_name']['p']
        ).replace(
            self.TEXT_EXPRESSION, child_text
        )
        return paragraph


class HeadingBuilder(IBuilder):
    """ hタグ(ヘッダ)の組み立てを責務に持つ """

    HEADING_EXPRESSION = '{h}'
    CLASSNAME_EXPRESSION = '{classname}'
    TEXT_EXPRESSION = '{text}'
    # example
    # <h2 class="...">
    #     概要
    # </h2>
    TEMPLATE = (
        f'<{HEADING_EXPRESSION} class="{CLASSNAME_EXPRESSION}">{LINE_BREAK}'
        f'{INDENT}{TEXT_EXPRESSION}{LINE_BREAK}'
        f'</{HEADING_EXPRESSION}>'
    )

    def is_target(self, block: Block) -> bool:
        return isinstance(block, HeadingBlock)

    def build(self, block: HeadingBlock, child_text: str) -> str:
        """
        ヘッダのHTML文字列を組み立て

        :param block: 組み立て元Block要素
        :param child_text: 子要素文字列
        :return: HTMLのヘッダタグを含む文字列
        """

        heading_tag = f'h{block.size}'
        heading = self.TEMPLATE.replace(
            self.HEADING_EXPRESSION, heading_tag
        ).replace(
            self.CLASSNAME_EXPRESSION, setting['class_name'].get(heading_tag, '')
        ).replace(
            self.TEXT_EXPRESSION, child_text
        )

        return heading


class QuoteBuilder(IBuilder):
    """ blockquote(引用)タグの組み立てを責務に持つ """

    # 子が複数行存在するため、改行やインデントは、コンバータや、他のビルダが責務を持つ
    TEXT_EXPRESSION = '{text}'
    CLASSNAME_EXPRESSION = '{classname}'
    # example
    # <blockquote class="...">
    #     引用
    # </blockquote>
    TEMPLATE = (
        f'<blockquote class="{CLASSNAME_EXPRESSION}">{LINE_BREAK}'
        f'{TEXT_EXPRESSION}'
        f'</blockquote>'
    )

    def is_target(self, block: Block) -> bool:
        return isinstance(block, QuoteBlock)

    def build(self, block: QuoteBlock, child_text: str) -> str:
        """
        引用要素のHTML文字列を組み立て

        :param block: 組み立て元Block要素
        :param child_text: 子要素文字列
        :return: HTMLのblockquoteタグを含む文字列
        """

        blockquote = self.TEMPLATE.replace(
            self.CLASSNAME_EXPRESSION, setting['class_name']['blockquote']
        ).replace(
            self.TEXT_EXPRESSION, child_text
        )

        return blockquote


class ListBuilder(IBuilder):
    """ ul(リスト)タグの組み立てを責務に持つ """

    TEXT_EXPRESSION = '{text}'
    CLASSNAME_EXPRESSION = '{classname}'
    # 子の改行/インデントはListItemBuilderが責務を持つ
    # example
    # <ul class="...">
    #     <li class="...">
    #         list item
    #     </li>
    # </ul>
    TEMPLATE = (
        f'<ul class="{CLASSNAME_EXPRESSION}">{LINE_BREAK}'
        f'{TEXT_EXPRESSION}'
        f'</ul>'
    )

    def is_target(self, block: Block) -> bool:
        return isinstance(block, ListBlock)

    def build(self, block: ListBlock, child_text: str) -> str:
        """
        リスト要素のHTML文字列を組み立て\n
        子要素liの組み立てはListItemBuilderへ委譲

        :param block: 組み立て元Block要素
        :param child_text: 子要素文字列
        :return: HTMLのulタグを含む文字列
        """

        unordered_list = self.TEMPLATE.replace(
            self.CLASSNAME_EXPRESSION, setting['class_name']['ul']
        ).replace(
            self.TEXT_EXPRESSION, child_text
        )

        return unordered_list


class ListItemBuilder(IBuilder):
    """ li(リスト子要素)タグの組み立てを責務に持つ """

    INDENT_EXPRESSION = '{indent}'
    CLASSNAME_EXPRESSION = '{classname}'
    TEXT_EXPRESSION = '{text}'
    # example
    # <li class="...">
    #     item1
    # </li>
    TEMPLATE = (
        f'{INDENT_EXPRESSION}<li class="{CLASSNAME_EXPRESSION}">{LINE_BREAK}'
        f'{INDENT_EXPRESSION}{INDENT}{TEXT_EXPRESSION}{LINE_BREAK}'
        f'{INDENT_EXPRESSION}</li>'
    )

    def is_target(self, block: Block) -> bool:
        return isinstance(block, ListItemBlock)

    def build(self, block: ListItemBlock, child_text: str) -> str:
        """
        リスト子要素のHTML文字列を組み立て

        :param block: 組み立て元Block要素
        :param child_text: 子要素文字列
        :return: HTMLのliタグを含む文字列
        """

        list_item = self.TEMPLATE.replace(
            self.INDENT_EXPRESSION, get_indent_text_from_depth(block.indent_depth)
        ).replace(
            self.CLASSNAME_EXPRESSION, setting['class_name']['li']
        ).replace(
            self.TEXT_EXPRESSION, child_text
        )

        return list_item


class CodeBlockBuilder(IBuilder):
    """ pre, code(コードブロック) 要素の組み立てを責務に持つ """

    TEXT_EXPRESSION = '{text}'
    LANGUAGE_EXPRESSION = '{language}'
    # 子要素は複数行に及ぶため、改行/インデントはPlainBlock側が責務を持つ
    # example
    # <pre>
    #     <code>
    #         const i = 0;
    #     </code>
    # </pre>
    TEMPLATE = (
        f'<pre>{LINE_BREAK}'
        f'{INDENT}<code class="{LANGUAGE_EXPRESSION}">{LINE_BREAK}'
        f'{TEXT_EXPRESSION}'
        f'{INDENT}</code>{LINE_BREAK}'
        f'</pre>'
    )

    def is_target(self, block: Block) -> bool:
        return isinstance(block, CodeBlock)

    def build(self, block: CodeBlock, child_text: str) -> str:
        """
        コードブロック要素のHTML文字列を組み立て

        :param block: 組み立て元Block要素
        :param child_text: 子要素文字列
        :return: HTMLのpre, codeタグを含む文字列
        """

        # highlight.jsでハイライトするとき、言語名は小文字を指定
        language_class_name = setting['class_name_with_template']['code_block'].replace(
            self.LANGUAGE_EXPRESSION, block.language.lower()
        )

        code_block = self.TEMPLATE.replace(
            self.LANGUAGE_EXPRESSION, language_class_name
        ).replace(
            self.TEXT_EXPRESSION, child_text
        )

        return code_block


class HorizontalRuleBuilder(IBuilder):
    """ hrタグで表現される水平罫線要素を生成することを責務に持つ """

    CLASSNAME_EXPRESSION = '{classname}'
    TEMPLATE = f'<hr class="{CLASSNAME_EXPRESSION}">'

    def is_target(self, block: Block) -> bool:
        return isinstance(block, HorizontalRuleBlock)

    def build(self, block: HorizontalRuleBlock, child_text: str) -> str:
        """
        hrタグ文字列を組み立て

        :param block: 組み立て元Block要素
        :param child_text: 子要素文字列
        :return: hrタグ文字列
        """

        return self.TEMPLATE.replace(self.CLASSNAME_EXPRESSION, setting['class_name']['hr'])
