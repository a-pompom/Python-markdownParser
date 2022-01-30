import pytest

from a_pompom_markdown_parser.html.block_builder import BlockBuilder, HeadingBuilder, QuoteBuilder, ListBuilder, ListItemBuilder, \
    CodeBlockBuilder, HorizontalRuleBuilder
from a_pompom_markdown_parser.converter.converter import Converter
from a_pompom_markdown_parser.element.block import CodeBlock
from a_pompom_markdown_parser.markdown.block_parser import BlockParser, HeadingParser, QuoteParser, ListParser, HorizontalRuleParser, \
    CodeBlockParser
from a_pompom_markdown_parser.markdown.inline_parser import InlineParser
from a_pompom_markdown_parser.markdown.parser import MarkdownParser

from a_pompom_markdown_parser.settings import setting

from tests.factory.block_factory import ListItemFactory

# よく使う設定値
LINE_BREAK = setting['newline_code']
INDENT = setting['indent']


class TestBlockBuilder:
    """ Block要素からHTML文字列が得られるか検証 """

    # HTML文字列組み立て
    @pytest.mark.parametrize(
        ('block_text', 'child_text', 'expected'),
        [
            (
                'plain text',
                'plain text',
                f'<p class="{setting["class_name"]["p"]}">{LINE_BREAK}{INDENT}plain text{LINE_BREAK}</p>'
            ),
            (
                '# 概要',
                '概要',
                (
                    f'<h1 class="{setting["class_name"]["h1"]}">{LINE_BREAK}'
                    f'{INDENT}概要{LINE_BREAK}'
                    f'</h1>'
                )
            ),
            (
                '> と言いました',
                'と言いました',
                (
                    f'<blockquote class="{setting["class_name"]["blockquote"]}">{LINE_BREAK}'
                    f'と言いました'
                    f'</blockquote>'
                )
            )
        ],
        ids=['plain', 'heading', 'quote'])
    def test_build(self, block_text: str, child_text: str, expected: str):
        # GIVEN
        sut = BlockBuilder()
        block = BlockParser().parse(block_text, InlineParser().parse(child_text))
        # WHEN
        actual = sut.build(block, child_text)
        # THEN
        assert actual == expected


class TestHeadingBuilder:
    """ HeadingBlock要素からヘッダと対応するHTML文字列を組み立てられるか検証 """

    # 対象判定
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            (
                '# this is a heading',
                True
            ),
            (
                'plain text',
                False
            ),
        ],
        ids=['target', 'not target'])
    def test_target(self, text: str, expected: bool):
        # GIVEN
        sut = HeadingBuilder()
        parser = BlockParser()
        child_text = parser.extract_inline_text(text)
        block = parser.parse(text, InlineParser().parse(child_text))

        # WHEN
        actual = sut.is_target(block)
        # THEN
        assert actual == expected

    # HTML文字列組み立て
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            (
                '# first heading',
                (
                    f'<h1 class="{setting["class_name"]["h1"]}">{LINE_BREAK}'
                    f'{INDENT}first heading{LINE_BREAK}'
                    f'</h1>'
                )
            ),
            (
                '#### 補足: これは補足です',
                (
                    f'<h4 class="{setting["class_name"]["h4"]}">{LINE_BREAK}'
                    f'{INDENT}補足: これは補足です{LINE_BREAK}'
                    f'</h4>'
                )
            )
        ],
        ids=['first', '4th'])
    def test_build(self, text: str, expected: str):
        # GIVEN
        sut = HeadingBuilder()
        parser = HeadingParser()
        child_text = parser.extract_text(text)
        block = HeadingParser().parse(text, InlineParser().parse(child_text))

        # WHEN
        actual = sut.build(block, child_text)
        # THEN
        assert actual == expected


class TestQuoteBuilder:
    """ blockquoteタグ文字列の組み立てを検証 """

    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            (
                '> これは引用です',
                True
            ),
            (
                '[参考](url)',
                False
            )
        ],
        ids=['target', 'not target']
    )
    def test_is_target(self, text: str, expected: bool):
        # GIVEN
        sut = QuoteBuilder()
        parser = BlockParser()
        child_text = parser.extract_inline_text(text)
        block = parser.parse(text, InlineParser().parse(child_text))

        # WHEN
        actual = sut.is_target(block)
        # THEN
        assert actual == expected

    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            (
                '> それが問題です',
                (
                    f'<blockquote class="{setting["class_name"]["blockquote"]}">{LINE_BREAK}'
                    f'それが問題です'
                    f'</blockquote>'
                )
            )
        ]
    )
    def test_build(self, text: str, expected: str):
        # GIVEN
        sut = QuoteBuilder()
        parser = QuoteParser()
        child_text = parser.extract_text(text)
        block = parser.parse(text, InlineParser().parse(child_text))

        # WHEN
        actual = sut.build(block, child_text)
        # THEN
        assert actual == expected


class TestListBuilder:
    """ ulタグ文字列要素の組み立て """

    # 対象判定
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            (
                '* task1',
                True
            ),
            ('やること',
             False
             ),
        ],
        ids=['target', 'not target']
    )
    def test_is_target(self, text: str, expected: bool):
        sut = ListBuilder()
        parser = BlockParser()
        child_text = parser.extract_inline_text(text)
        block = parser.parse(text, InlineParser().parse(child_text))

        # WHEN
        actual = sut.is_target(block)
        # THEN
        assert actual == expected

    # ビルド結果
    # 要素自体の改行/インデントは子要素のビルダが担う
    # これは、子要素のliは複数行に及び、子要素1行分に対してのみ改行やインデントを適用するとかえって扱いづらくなるためである
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            (
                '- no.1',
                (
                    f'<ul class="{setting["class_name"]["ul"]}">{LINE_BREAK}'
                    f'no.1'
                    f'</ul>'
                )
            )
        ]
    )
    def test_build(self, text: str, expected: str):
        # GIVEN
        sut = ListBuilder()
        parser = ListParser()
        child_text = parser.extract_text(text)
        block = parser.parse(text, InlineParser().parse(child_text))

        # WHEN
        actual = sut.build(block, child_text)
        # THEN
        assert actual == expected


class TestListItemBuilder:
    """ liタグ文字列要素の組み立て """

    # ビルド対象
    @pytest.mark.parametrize(
        'text',
        ['最初の要素']
    )
    def test_is_target_list_item(self, text: str):
        sut = ListItemBuilder()
        block = ListItemFactory().create_single_list_item(text)
        # WHEN
        actual = sut.is_target(block)
        # THEN
        assert actual is True

    # ビルド対象でない
    @pytest.mark.parametrize(
        'text',
        [
            '* 1st element'
        ]
    )
    def test_is_target_not_list_item(self, text: str):
        sut = ListItemBuilder()
        parser = BlockParser()
        child_text = parser.extract_inline_text(text)
        block = parser.parse(text, InlineParser().parse(child_text))

        # WHEN
        actual = sut.is_target(block)
        # THEN
        assert actual is False

    # ビルド結果
    # li要素はulの子となることが前提なので、インデント階層を含む
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            (
                'やりたいことその1',
                (
                    f'{INDENT}<li class="{setting["class_name"]["li"]}">{LINE_BREAK}'
                    f'{INDENT}{INDENT}やりたいことその1{LINE_BREAK}'
                    f'{INDENT}</li>'
                )
            )
        ],
        ids=['list item']
    )
    def test_build(self, text: str, expected: str):
        # GIVEN
        sut = ListItemBuilder()
        block = ListItemFactory().create_single_list_item(text)
        # WHEN
        actual = sut.build(block, text)
        # THEN
        assert actual == expected


class TestCodeBlockBuilder:
    """ pre, codeタグ文字列を組み立てられるか """

    # ビルド対象
    @pytest.mark.parametrize(
        'text',
        [
            '```Java',
            '```',
        ]
    )
    def test_is_target_target(self, text: str):
        # GIVEN
        sut = CodeBlockBuilder()
        block = CodeBlockParser().parse(text, InlineParser().parse(''))
        # WHEN
        actual = sut.is_target(block)
        # THEN
        assert actual is True

    # ビルド対象でない
    @pytest.mark.parametrize(
        'text',
        [
            '## 概要',
            '// コメントだけれどコードではない',
        ]
    )
    def test_is_target_not_target(self, text: str):
        # GIVEN
        sut = CodeBlockBuilder()
        parser = BlockParser()
        child_text = parser.extract_inline_text(text)
        block = parser.parse(text, InlineParser().parse(child_text))

        # WHEN
        actual = sut.is_target(block)
        # THEN
        assert actual is False

    # pre, codeタグ文字列の組み立て
    # 要素自体の改行/インデントはconverterが責務を持つ
    # これは、子要素は複数行に及び、子要素1行分に対してのみ改行やインデントを適用するとかえって扱いづらくなるためである
    @pytest.mark.parametrize(
        ('lines', 'child_text', 'expected'),
        [
            (
                [
                    '```Java',
                    'List<String> list;',
                    '```',
                ],
                'List<String> list;',
                (
                    f'<pre>{LINE_BREAK}'
                    f'{INDENT}<code class="language-java hljs">{LINE_BREAK}'
                    f'List<String> list;'
                    f'{INDENT}</code>{LINE_BREAK}'
                    f'</pre>'
                )
            ),
            (
                [
                    '```',
                    '## [参考](url)',
                    '```'
                ],
                '## [参考](url)',
                (
                    f'<pre>{LINE_BREAK}'
                    f'{INDENT}<code class="language- hljs">{LINE_BREAK}'
                    f'## [参考](url)'
                    f'{INDENT}</code>{LINE_BREAK}'
                    f'</pre>'
                )
            ),

        ],
        ids=['code', 'markdown text']
    )
    def test_build(self, lines: list[str], child_text: str, expected: str):
        # GIVEN
        sut = CodeBlockBuilder()
        code_block = Converter().convert(MarkdownParser().parse(lines)).content[0]

        if not isinstance(code_block, CodeBlock):
            assert False
        # WHEN
        actual = sut.build(code_block, child_text)
        # THEN
        assert actual == expected


class TestHorizontalRuleBuilder:
    """ HorizontalRuleBlock要素からhrタグと対応するHTML文字列が得られるか検証 """

    # 対象判定
    @pytest.mark.parametrize(
        ('text', 'expected'), [
            ('---', True),
            ('--', False),
        ],
        ids=['target', 'not target'])
    def test_target(self, text: str, expected: bool):
        # GIVEN
        sut = HorizontalRuleBuilder()
        block = BlockParser().parse(text, InlineParser().parse(text))
        # WHEN
        actual = sut.is_target(block)
        # THEN
        assert actual == expected

    # HTML組み立て
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            (
                '---',
                f'<hr class="{setting["class_name"]["hr"]}">'
            ),
        ]
    )
    def test_build(self, text: str, expected: str):
        # GIVEN
        sut = HorizontalRuleBuilder()
        block = HorizontalRuleParser().parse(text, InlineParser().parse(''))
        # WHEN
        actual = sut.build(block, '')
        # THEN
        assert actual == expected
