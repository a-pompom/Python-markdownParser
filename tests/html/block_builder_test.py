import pytest

from a_pompom_markdown_parser.html.block_builder import BlockBuilder, HeadingBuilder, QuoteBuilder, ListBuilder, \
    ListItemBuilder, CodeBlockBuilder, HorizontalRuleBuilder
from a_pompom_markdown_parser.element.block import Block, HeadingBlock, CodeBlock, HorizontalRuleBlock, ParagraphBlock, \
    QuoteBlock, ListBlock, ListItemBlock, PlainBlock
from a_pompom_markdown_parser.element.inline import PlainInline, LinkInline

from a_pompom_markdown_parser.settings import setting

# よく使う設定値
LINE_BREAK = setting['newline_code']
INDENT = setting['indent']


class TestBlockBuilder:
    """ Block要素からHTML文字列が得られるか検証 """

    # HTML文字列組み立て
    @pytest.mark.parametrize(
        ('block', 'child_text', 'expected'),
        [
            (
                ParagraphBlock(indent_depth=0, children=[
                    PlainInline(text='plain text')
                ]),
                'plain text',
                (f'<p'
                 f' class="{setting["class_name"]["p"]}">{LINE_BREAK}'
                 f'{INDENT}plain text{LINE_BREAK}'
                 f'</p>')
            ),
            (
                HeadingBlock(size=1, children=[
                    PlainInline(text='概要')
                ]),
                '概要',
                (
                    f'<h1 id="概要" class="{setting["class_name"]["h1"]}">{LINE_BREAK}'
                    f'{INDENT}概要{LINE_BREAK}'
                    f'</h1>'
                )
            ),
            (
                QuoteBlock(children=[
                    ParagraphBlock(indent_depth=0, children=[
                        PlainInline(text='と言いました')
                    ])
                ]),
                'と言いました',
                (
                    f'<blockquote class="{setting["class_name"]["blockquote"]}">{LINE_BREAK}'
                    f'と言いました'
                    f'</blockquote>'
                )
            )
        ],
        ids=['plain', 'heading', 'quote'])
    def test_build(self, block: Block, child_text: str, expected: str):
        # GIVEN
        sut = BlockBuilder()
        # WHEN
        actual = sut.build(block, child_text)
        # THEN
        assert actual == expected


class TestHeadingBuilder:
    """ HeadingBlock要素からヘッダと対応するHTML文字列を組み立てられるか検証 """

    # 対象判定
    @pytest.mark.parametrize(
        ('block', 'expected'),
        [
            (
                HeadingBlock(size=1, children=[
                    PlainInline(text='this is a heading')
                ]),
                True
            ),
            (
                ParagraphBlock(indent_depth=0, children=[
                    PlainInline(text='plain text')
                ]),
                False
            ),
        ],
        ids=['target', 'not target'])
    def test_target(self, block: Block, expected: bool):
        # GIVEN
        sut = HeadingBuilder()

        # WHEN
        actual = sut.is_target(block)
        # THEN
        assert actual == expected

    # HTML文字列組み立て
    @pytest.mark.parametrize(
        ('block', 'child_text', 'expected'),
        [
            (
                HeadingBlock(size=1, children=[
                    PlainInline(text='first heading')
                ]),
                'first heading',
                (
                    f'<h1 id="first heading" class="{setting["class_name"]["h1"]}">{LINE_BREAK}'
                    f'{INDENT}first heading{LINE_BREAK}'
                    f'</h1>'
                )
            ),
            (
                HeadingBlock(size=4, children=[
                    PlainInline(text='補足: これは補足です')
                ]),
                '補足: これは補足です',
                (
                    f'<h4 id="補足: これは補足です" class="{setting["class_name"]["h4"]}">{LINE_BREAK}'
                    f'{INDENT}補足: これは補足です{LINE_BREAK}'
                    f'</h4>'
                )
            )
        ],
        ids=['first', '4th'])
    def test_build(self, block: HeadingBlock, child_text: str, expected: str):
        # GIVEN
        sut = HeadingBuilder()
        # WHEN
        actual = sut.build(block, child_text)
        # THEN
        assert actual == expected


class TestQuoteBuilder:
    """ blockquoteタグ文字列の組み立てを検証 """

    @pytest.mark.parametrize(
        ('block', 'expected'),
        [
            (
                QuoteBlock(children=[
                    PlainInline(text='これは引用です')
                ]),
                True
            ),
            (
                ParagraphBlock(children=[
                    LinkInline(href='url', text='参考')
                ]),
                False
            )
        ],
        ids=['target', 'not target']
    )
    def test_is_target(self, block: Block, expected: bool):
        # GIVEN
        sut = QuoteBuilder()
        # WHEN
        actual = sut.is_target(block)
        # THEN
        assert actual == expected

    @pytest.mark.parametrize(
        ('block', 'child_text', 'expected'),
        [
            (
                QuoteBlock(children=[
                    PlainInline(text='それが問題です')
                ]),
                'それが問題です',
                (
                    f'<blockquote class="{setting["class_name"]["blockquote"]}">{LINE_BREAK}'
                    f'それが問題です'
                    f'</blockquote>'
                )
            )
        ]
    )
    def test_build(self, block: QuoteBlock, child_text: str, expected: str):
        # GIVEN
        sut = QuoteBuilder()
        # WHEN
        actual = sut.build(block, child_text)
        # THEN
        assert actual == expected


class TestListBuilder:
    """ ulタグ文字列要素の組み立て """

    # 対象判定
    @pytest.mark.parametrize(
        ('block', 'expected'),
        [
            (
                ListBlock(indent_depth=0, children=[
                    ListItemBlock(indent_depth=1, children=[
                        PlainInline(text='task1')
                    ])
                ]),
                True
            ),
            (
                ParagraphBlock(indent_depth=0, children=[
                    PlainInline(text='やること')
                ]),
                False
            ),
        ],
        ids=['target', 'not target']
    )
    def test_is_target(self, block: Block, expected: bool):
        # GIVEN
        sut = ListBuilder()
        # WHEN
        actual = sut.is_target(block)
        # THEN
        assert actual == expected

    # ビルド結果
    # 要素自体の改行/インデントは子要素のビルダが担う
    # これは、子要素のliは複数行に及び、子要素1行分に対してのみ改行やインデントを適用するとかえって扱いづらくなるためである
    @pytest.mark.parametrize(
        ('block', 'child_text', 'expected'),
        [
            (
                ListBlock(indent_depth=0, children=[
                    PlainInline(text='no.1')
                ]),
                'no.1',
                (
                    f'<ul class="{setting["class_name"]["ul"]}">{LINE_BREAK}'
                    f'no.1'
                    f'</ul>'
                )
            )
        ]
    )
    def test_build(self, block: ListBlock, child_text: str, expected: str):
        # GIVEN
        sut = ListBuilder()
        # WHEN
        actual = sut.build(block, child_text)
        # THEN
        assert actual == expected


class TestListItemBuilder:
    """ liタグ文字列要素の組み立て """

    # ビルド対象
    @pytest.mark.parametrize(
        ('block', 'expected'),
        [
            (
                ListItemBlock(indent_depth=0, children=[
                    PlainInline(text='item1')
                ]),
                True
            ),
            (
                ParagraphBlock(indent_depth=0, children=[
                    PlainInline(text='item')
                ]),
                False
            )
        ],
        ids=['target', 'not target']
    )
    def test_is_target(self, block: Block, expected: bool):
        # GIVEN
        sut = ListItemBuilder()
        # WHEN
        actual = sut.is_target(block)
        # THEN
        assert actual == expected

    # ビルド結果
    # li要素はulの子となることが前提なので、インデント階層を含む
    @pytest.mark.parametrize(
        ('block', 'child_text', 'expected'),
        [
            (
                ListItemBlock(indent_depth=1, children=[
                    PlainInline(text='やりたいことその1')
                ]),
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
    def test_build(self, block: ListItemBlock, child_text: str, expected: str):
        # GIVEN
        sut = ListItemBuilder()
        # WHEN
        actual = sut.build(block, child_text)
        # THEN
        assert actual == expected


class TestCodeBlockBuilder:
    """ pre, codeタグ文字列を組み立てられるか """

    # ビルド対象か
    @pytest.mark.parametrize(
        ('block', 'expected'),
        [
            (
                CodeBlock(language='Java', children=[
                    PlainBlock(indent_depth=0, children=[
                        PlainInline(text='// java comment')
                    ])
                ]),
                True
            ),
            (
                HeadingBlock(size=1, children=[
                    PlainInline(text='not code')
                ]),
                False
            )
        ]
    )
    def test_is_target(self, block: Block, expected: bool):
        # GIVEN
        sut = CodeBlockBuilder()
        # WHEN
        actual = sut.is_target(block)
        # THEN
        assert actual == expected

    # pre, codeタグ文字列の組み立て
    # 要素自体の改行/インデントはconverterが責務を持つ
    # これは、子要素は複数行に及び、子要素1行分に対してのみ改行やインデントを適用するとかえって扱いづらくなるためである
    @pytest.mark.parametrize(
        ('block', 'child_text', 'expected'),
        [
            (
                CodeBlock(language='Java', children=[
                    PlainBlock(indent_depth=0, children=[
                        PlainInline(text='List<String> list;')
                    ])
                ]),
                'List<String> list;',
                (
                    f'<pre>{LINE_BREAK}'
                    f'{INDENT}<code class="language-java hljs">'
                    f'List<String> list;'
                    f'{INDENT}</code>{LINE_BREAK}'
                    f'</pre>'
                )
            ),
            (
                CodeBlock(language='', children=[
                    PlainBlock(indent_depth=0, children=[
                        PlainInline(text='## [参考](url)')
                    ])
                ]),
                '## [参考](url)',
                (
                    f'<pre>{LINE_BREAK}'
                    f'{INDENT}<code class="language- hljs">'
                    f'## [参考](url)'
                    f'{INDENT}</code>{LINE_BREAK}'
                    f'</pre>'
                )
            ),

        ],
        ids=['code', 'markdown text']
    )
    def test_build(self, block: CodeBlock, child_text: str, expected: str):
        # GIVEN
        sut = CodeBlockBuilder()
        # WHEN
        actual = sut.build(block, child_text)
        # THEN
        assert actual == expected


class TestHorizontalRuleBuilder:
    """ HorizontalRuleBlock要素からhrタグと対応するHTML文字列が得られるか検証 """

    # 対象判定
    @pytest.mark.parametrize(
        ('block', 'expected'), [
            (
                HorizontalRuleBlock(children=[
                    PlainInline(text='')
                ]),
                True
            ),
            (
                ParagraphBlock(indent_depth=0, children=[
                    PlainInline(text='--')
                ]),
                False
            )
        ],
        ids=['target', 'not target'])
    def test_target(self, block: Block, expected: bool):
        # GIVEN
        sut = HorizontalRuleBuilder()
        # WHEN
        actual = sut.is_target(block)
        # THEN
        assert actual == expected

    # HTML組み立て
    @pytest.mark.parametrize(
        ('block', 'expected'),
        [
            (
                HorizontalRuleBlock(children=[
                    PlainInline(text='')
                ]),
                f'<hr class="{setting["class_name"]["hr"]}">'
            ),
        ]
    )
    def test_build(self, block: HorizontalRuleBlock, expected: str):
        # GIVEN
        sut = HorizontalRuleBuilder()
        # WHEN
        actual = sut.build(block, '')
        # THEN
        assert actual == expected
