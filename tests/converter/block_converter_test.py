import pytest

from a_pompom_markdown_parser.converter.converter import group_same_range_blocks
from a_pompom_markdown_parser.element.block import Block, ParagraphBlock, QuoteBlock, ListBlock, \
    ListItemBlock, CodeBlock, PlainBlock
from a_pompom_markdown_parser.element.inline import PlainInline
from a_pompom_markdown_parser.converter.block_converter import BlockConverter, QuoteConverter, ListConverter, \
    CodeBlockConverter
from a_pompom_markdown_parser.markdown.parser import MarkdownParser


class TestBlockConverter:
    """
    Block要素のコンバータ
    本モジュールへの入力は、サブリスト構築関数により、同種のBlock要素のリストが渡される
    よって、テストでは同種のBlock要素のリストのみ検証
    """

    @pytest.mark.parametrize(
        ('lines', 'expected_list'),
        [
            (
                ['今日はいい天気です。', '日記を終わります。'],
                [
                    ParagraphBlock(indent_depth=0, children=[
                        PlainInline(text='今日はいい天気です。')
                    ]),
                    ParagraphBlock(indent_depth=0, children=[
                        PlainInline(text='日記を終わります。')
                    ])
                ]
            ),

            (
                ['> いい感じの言葉を', '> 引用します。'],
                [
                    QuoteBlock(children=[
                        ParagraphBlock(indent_depth=1, children=[
                            PlainInline(text='いい感じの言葉を')
                        ]),
                        ParagraphBlock(indent_depth=1, children=[
                            PlainInline(text='引用します。')
                        ])
                    ])
                ]
            ),

            (
                ['* 1st', '* 2nd', '* 3rd'],
                [
                    ListBlock(indent_depth=0, children=[
                        ListItemBlock(indent_depth=1, children=[
                            PlainInline(text='1st')
                        ]),
                        ListItemBlock(indent_depth=1, children=[
                            PlainInline(text='2nd')
                        ]),
                        ListItemBlock(indent_depth=1, children=[
                            PlainInline(text='3rd')
                        ]),
                    ])
                ]
            ),
        ],
        ids=['plain', 'quote', 'list']
    )
    def test_convert(self, lines: list[str], expected_list: list[Block]):
        # GIVEN
        sut = BlockConverter()
        markdown_result = MarkdownParser().parse(lines)
        # WHEN
        actual_list = sut.convert(markdown_result.content)
        # THEN
        for actual, expected in zip(actual_list, expected_list):
            assert actual == expected


class TestQuoteConverter:
    """ 引用要素のコンバータ """

    # Block要素群が変換対象か
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (['> quote text', '> 引用文です。'], True),
            (['plain text', 'plain 2nd line text'], False)
        ],
        ids=['target', 'not target']
    )
    def test_is_target(self, lines: list[str], expected: bool):
        # GIVEN
        markdown_result = MarkdownParser().parse(lines)
        sut = QuoteConverter()
        # WHEN
        actual = sut.is_target(markdown_result.content)
        # THEN
        assert actual == expected

    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (
                ['> quote text'],
                QuoteBlock(children=[
                    ParagraphBlock(indent_depth=1, children=[
                        PlainInline(text='quote text')
                    ])
                ])
            ),
            (
                ['> Pythonは', '> プログラミング言語です'],
                QuoteBlock(children=[
                    ParagraphBlock(indent_depth=1, children=[
                        PlainInline(text='Pythonは')
                    ]),
                    ParagraphBlock(indent_depth=1, children=[
                        PlainInline(text='プログラミング言語です')
                    ])
                ])
            ),
        ],
        ids=['single', 'multiple']
    )
    def test_convert(self, lines: list[str], expected: QuoteBlock):
        # GIVEN
        sut = QuoteConverter()
        markdown_result = MarkdownParser().parse(lines)

        if not sut.is_target(markdown_result.content):
            assert False

        # WHEN
        # 「Python3.10-dev, PyCharm2021.2」の段階ではリストに対する型ガードが
        # 有効にならないようなので、型チェックを無効化
        # noinspection PyTypeChecker
        actual = sut.convert(markdown_result.content)
        # THEN
        assert actual == expected


class TestListConverter:
    """ リスト要素のコンバータ """

    # Block要素群が変換対象か
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (['* 1st element', '* 2nd element'], True),
            (['# Heading', 'Paragraph'], False),
        ],
        ids=['target', 'not target']
    )
    def test_is_target(self, lines: list[str], expected: bool):
        # GIVEN
        sut = ListConverter()
        markdown_result = MarkdownParser().parse(lines)
        # WHEN
        actual = sut.is_target(markdown_result.content)
        # THEN
        assert actual == expected

    # リスト・リスト子要素へ変換
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (
                ['- method1'],
                ListBlock(indent_depth=0, children=[
                    ListItemBlock(indent_depth=1, children=[
                        PlainInline(text='method1')
                    ])
                ])
            ),
            (
                ['* item1', '* item2'],
                ListBlock(indent_depth=0, children=[
                    ListItemBlock(indent_depth=1, children=[
                        PlainInline(text='item1')
                    ]),
                    ListItemBlock(indent_depth=1, children=[
                        PlainInline(text='item2')
                    ])
                ])
            ),
        ],
        ids=['single', 'multiple']
    )
    def test_convert(self, lines: list[str], expected: ListBlock):
        sut = ListConverter()
        markdown_result = MarkdownParser().parse(lines)

        if not sut.is_target(markdown_result.content):
            assert False

        # WHEN
        # 「Python3.10-dev, PyCharm2021.2」の段階ではリストに対する型ガードが
        # 有効にならないようなので、型チェックを無効化
        # noinspection PyTypeChecker
        actual = sut.convert(markdown_result.content)
        # THEN
        assert actual == expected


class TestCodeBlockConverter:
    """ コードブロック要素へ統合できるか """

    # 対象判定-対象
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (
                [
                    '```JavaScript',
                    'const i = 0;',
                    '// comment',
                    '```'
                ],
                True
            ),
        ],
    )
    def test_is_target_code_block(self, lines: list[str], expected: bool):
        # GIVEN
        sut = CodeBlockConverter()
        blocks = group_same_range_blocks(MarkdownParser().parse(lines).content)
        # WHEN
        actual = sut.is_target(blocks)
        # THEN
        assert actual == expected

    # 対象判定-対象外
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (['## Heading text', 'Plain text'], False),
        ]
    )
    def test_is_target_not_code_block(self, lines: list[str], expected: bool):
        # GIVEN
        sut = CodeBlockConverter()
        blocks = MarkdownParser().parse(lines).content
        # WHEN
        actual = sut.is_target(blocks)
        # THEN
        assert actual == expected

    # 1つのコードブロックへ統合されるか
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (
                ['```Python', '# comment', 'instance = Klass()', '```'],
                CodeBlock(language='Python', children=[
                    PlainBlock(indent_depth=0, children=[
                        PlainInline(text='# comment')
                    ]),
                    PlainBlock(indent_depth=0, children=[
                        PlainInline(text='instance = Klass()')
                    ])
                ])
            ),
            (
                ['```', '## [参考](url)', '> 引用ここまで'],
                CodeBlock(language='', children=[
                    PlainBlock(indent_depth=0, children=[
                        PlainInline(text='## [参考](url)')
                    ]),
                    PlainBlock(indent_depth=0, children=[
                        PlainInline(text='> 引用ここまで')
                    ])
                ])
            ),
        ],
        ids=['code', 'not parsed']
    )
    def test_convert(self, lines: list[str], expected: CodeBlock):
        # GIVEN
        sut = CodeBlockConverter()
        blocks = group_same_range_blocks(MarkdownParser().parse(lines).content)

        if not sut.is_target(blocks):
            assert False

        # WHEN
        # 「Python3.10-dev, PyCharm2021.2」の段階ではリストに対する型ガードが
        # 有効にならないようなので、型チェックを無効化
        # noinspection PyTypeChecker
        actual = sut.convert(blocks)
        # THEN
        assert actual == expected
