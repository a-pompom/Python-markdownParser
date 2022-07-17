import pytest

from a_pompom_markdown_parser.element.block import Block, ParagraphBlock, QuoteBlock, ListBlock, \
    ListItemBlock, CodeBlock, PlainBlock, ParseResult, HeadingBlock, CodeChildBlock
from a_pompom_markdown_parser.element.inline import PlainInline
from a_pompom_markdown_parser.converter.block_converter import BlockConverter, QuoteConverter, ListConverter, \
    CodeBlockConverter


class TestBlockConverter:
    """
    Block要素のコンバータ
    本モジュールへの入力は、サブリスト構築関数により、同種のBlock要素のリストが渡される
    よって、テストでは同種のBlock要素のリストのみ検証
    """

    @pytest.mark.parametrize(
        ('parse_result', 'expected_list'),
        [
            (
                ParseResult(content=[
                    ParagraphBlock(indent_depth=0, children=[
                        PlainInline(text='今日はいい天気です。')
                    ]),
                    ParagraphBlock(indent_depth=0, children=[
                        PlainInline(text='日記を終わります。')
                    ]),
                ]),
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
                ParseResult(content=[
                    QuoteBlock(children=[
                        PlainInline('いい感じの言葉を')
                    ]),
                    QuoteBlock(children=[
                        PlainInline('引用します。')
                    ]),
                ]),
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
                ParseResult(content=[
                    ListBlock(indent_depth=0, children=[
                        PlainInline(text='1st')
                    ]),
                    ListBlock(indent_depth=0, children=[
                        PlainInline(text='2nd')
                    ]),
                    ListBlock(indent_depth=0, children=[
                        PlainInline(text='3rd')
                    ]),
                ]),
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
    def test_convert(self, parse_result: ParseResult, expected_list: list[Block]):
        # GIVEN
        sut = BlockConverter()
        # WHEN
        actual_list = sut.convert(parse_result.content)
        # THEN
        for actual, expected in zip(actual_list, expected_list):
            assert actual == expected


class TestQuoteConverter:
    """ 引用要素のコンバータ """

    # Block要素群が変換対象か
    @pytest.mark.parametrize(
        ('parse_result', 'expected'),
        [
            (
                ParseResult(content=[
                    QuoteBlock(children=[
                        PlainInline(text='これは引用要素です')
                    ]),
                    QuoteBlock(children=[
                        PlainInline(text='これも引用要素です')
                    ]),
                ]),
                True
            ),
            (
                ParseResult(content=[
                    ParagraphBlock(indent_depth=0, children=[
                        PlainInline(text='plain text')
                    ]),
                    QuoteBlock(children=[
                        PlainInline(text='これは引用要素です')
                    ]),
                ]),
                False
            )
        ],
        ids=['target', 'not target']

    )
    def test_is_target(self, parse_result: ParseResult, expected: bool):
        # GIVEN
        sut = QuoteConverter()
        # WHEN
        actual = sut.is_target(parse_result.content)
        # THEN
        assert actual == expected

    @pytest.mark.parametrize(
        ('parse_result', 'expected'),
        [
            (
                ParseResult(content=[
                    QuoteBlock(children=[
                        PlainInline(text='quote text')
                    ]),
                ]),
                QuoteBlock(children=[
                    ParagraphBlock(indent_depth=1, children=[
                        PlainInline(text='quote text')
                    ])
                ])
            ),

            (
                ParseResult(content=[
                    QuoteBlock(children=[
                        PlainInline(text='Pythonは')
                    ]),
                    QuoteBlock(children=[
                        PlainInline(text='プログラミング言語です')
                    ]),
                ]),
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
    def test_convert(self, parse_result: ParseResult, expected: QuoteBlock):
        # GIVEN
        sut = QuoteConverter()

        if not sut.is_target(parse_result.content):
            assert False

        # WHEN
        # 「Python3.10-dev, PyCharm2021.2」の段階ではリストに対する型ガードが
        # 有効にならないようなので、型チェックを無効化
        # noinspection PyTypeChecker
        actual = sut.convert(parse_result.content)
        # THEN
        assert actual == expected


class TestListConverter:
    """ リスト要素のコンバータ """

    # Block要素群が変換対象か
    @pytest.mark.parametrize(
        ('parse_result', 'expected'),
        [
            (
                ParseResult(content=[
                    ListBlock(indent_depth=0, children=[
                        PlainInline(text='1st element')
                    ]),
                    ListBlock(indent_depth=0, children=[
                        PlainInline(text='2nd element')
                    ]),
                ]),
                True
            ),
            (
                ParseResult(content=[
                    HeadingBlock(size=1, children=[
                        PlainInline(text='Heading')
                    ]),
                    ParagraphBlock(indent_depth=0, children=[
                        PlainInline(text='Paragraph')
                    ]),
                ]),
                False
            ),
        ],
        ids=['target', 'not target']
    )
    def test_is_target(self, parse_result: ParseResult, expected: bool):
        # GIVEN
        sut = ListConverter()
        # WHEN
        actual = sut.is_target(parse_result.content)
        # THEN
        assert actual == expected

    # リスト・リスト子要素へ変換
    @pytest.mark.parametrize(
        ('parse_result', 'expected'),
        [
            (
                ParseResult(content=[
                    ListBlock(indent_depth=0, children=[
                        PlainInline(text='method1')
                    ])
                ]),
                ListBlock(indent_depth=0, children=[
                    ListItemBlock(indent_depth=1, children=[
                        PlainInline(text='method1')
                    ])
                ])
            ),
            (
                ParseResult(content=[
                    ListBlock(children=[
                        PlainInline(text='item1')
                    ]),
                    ListBlock(children=[
                        PlainInline(text='item2')
                    ]),
                ]),
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
    def test_convert(self, parse_result: ParseResult, expected: ListBlock):
        sut = ListConverter()

        if not sut.is_target(parse_result.content):
            assert False

        # WHEN
        # 「Python3.10-dev, PyCharm2021.2」の段階ではリストに対する型ガードが
        # 有効にならないようなので、型チェックを無効化
        # noinspection PyTypeChecker
        actual = sut.convert(parse_result.content)
        # THEN
        assert actual == expected


class TestCodeBlockConverter:
    """ コードブロック要素へ統合できるか """

    # 対象判定-対象
    @pytest.mark.parametrize(
        ('parse_result', 'expected'),
        [
            (
                ParseResult(content=[
                    CodeBlock(language='JavaScript', children=[
                        PlainInline(text='')
                    ]),
                    CodeChildBlock(children=[
                        PlainInline(text='const i = 0;')
                    ]),
                    CodeChildBlock(children=[
                        PlainInline(text='// comment')
                    ]),
                ]),
                True
            ),
        ],
    )
    def test_is_target_code_block(self, parse_result: ParseResult, expected: bool):
        # GIVEN
        sut = CodeBlockConverter()
        # WHEN
        actual = sut.is_target(parse_result.content)
        # THEN
        assert actual == expected

    # 対象判定-対象外
    @pytest.mark.parametrize(
        ('parse_result', 'expected'),
        [
            (
                ParseResult(content=[
                    HeadingBlock(size=2, children=[
                        PlainInline(text='Heading text')
                    ]),
                    ParagraphBlock(indent_depth=0, children=[
                        PlainInline(text='Plain text')
                    ])
                ]),
                False
            ),
        ]
    )
    def test_is_target_not_code_block(self, parse_result: ParseResult, expected: bool):
        # GIVEN
        sut = CodeBlockConverter()
        # WHEN
        actual = sut.is_target(parse_result.content)
        # THEN
        assert actual == expected

    # 1つのコードブロックへ統合されるか
    @pytest.mark.parametrize(
        ('parse_result', 'expected'),
        [
            (
                ParseResult(content=[
                    CodeBlock(language='Python', children=[]),
                    CodeChildBlock(children=[
                        PlainInline(text='# comment')
                    ]),
                    CodeChildBlock(children=[
                        PlainInline(text='instance = Klass()')
                    ]),
                ]),
                CodeBlock(language='Python', children=[
                    PlainBlock(indent_depth=0, children=[
                        PlainInline(text='# comment')
                    ]),
                    PlainBlock(indent_depth=0, children=[
                        PlainInline(text='instance = Klass()')
                    ]),
                ])
            ),

            (
                ParseResult(content=[
                    CodeBlock(language='', children=[]),
                    CodeChildBlock(children=[
                        PlainInline(text='## [参考](url)')
                    ]),
                    CodeChildBlock(children=[
                        PlainInline(text='> 引用ここまで')
                    ]),
                ]),
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
        ids=['code', 'inline element not parsed']
    )
    def test_convert(self, parse_result: ParseResult, expected: CodeBlock):
        # GIVEN
        sut = CodeBlockConverter()

        if not sut.is_target(parse_result.content):
            assert False

        # WHEN
        # 「Python3.10-dev, PyCharm2021.2」の段階ではリストに対する型ガードが
        # 有効にならないようなので、型チェックを無効化
        # noinspection PyTypeChecker
        actual = sut.convert(parse_result.content)
        # THEN
        assert actual == expected
