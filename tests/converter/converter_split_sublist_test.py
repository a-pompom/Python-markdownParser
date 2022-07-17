import pytest

from a_pompom_markdown_parser.converter.converter import split_to_convert_target
from a_pompom_markdown_parser.element.block import Block, ParagraphBlock, QuoteBlock, CodeBlock, CodeChildBlock, \
    HeadingBlock, ParseResult
from a_pompom_markdown_parser.element.inline import PlainInline


# blockのリスト同士が同一とみなせるか判定
def assert_same_block_list(actual_list: list[Block], expected_list: list[Block]):
    for actual, expected in zip(actual_list, expected_list):
        assert actual == expected


class TestSplitToConvertTarget:
    """ コンバータで処理できるようBlockのリストを種別ごとに分割 """

    # 1種類のBlock要素のみで構成
    @pytest.mark.parametrize(
        ('parse_result', 'expected_list_of_list'),
        [
            (
                ParseResult(content=[
                    ParagraphBlock(indent_depth=0, children=[
                        PlainInline(text='first plain text')
                    ]),
                    ParagraphBlock(indent_depth=0, children=[
                        PlainInline(text='second plain text')
                    ]),
                ]),
                [
                    [
                        ParagraphBlock(indent_depth=0, children=[
                            PlainInline(text='first plain text')
                        ]),
                        ParagraphBlock(indent_depth=0, children=[
                            PlainInline(text='second plain text')
                        ])
                    ]
                ]
            ),
            (
                ParseResult(content=[
                    QuoteBlock(children=[
                        PlainInline(text='私は昨日')
                    ]),
                    QuoteBlock(children=[
                        PlainInline(text='こう言いました')
                    ]),
                ]),
                [
                    [
                        QuoteBlock(children=[
                            PlainInline(text='私は昨日')
                        ]),
                        QuoteBlock(children=[
                            PlainInline(text='こう言いました')
                        ]),
                    ]
                ]
            ),
            (
                ParseResult(content=[
                    CodeBlock(language='Python', children=[]),
                    CodeChildBlock(children=[
                        PlainInline(text='# TODO')
                    ])
                ]),
                [
                    [
                        CodeBlock(language='Python', children=[]),
                        CodeChildBlock(children=[
                            PlainInline(text='# TODO')
                        ])
                    ]
                ]
            ),
        ],
        ids=['only plain', 'only block quote', 'code block']
    )
    def test_only_single_type_block(self, parse_result: ParseResult, expected_list_of_list: list[list[Block]]):
        # GIVEN
        sut = split_to_convert_target

        # WHEN
        for convert_target, expected_list in zip(sut(parse_result.content), expected_list_of_list):
            # THEN
            assert_same_block_list(convert_target, expected_list)

    # 複数の種類のBlock要素が混在
    @pytest.mark.parametrize(
        ('parse_result', 'expected_list_of_list'),
        [
            (
                ParseResult(content=[
                    HeadingBlock(size=1, children=[
                        PlainInline(text='マークダウンとは')
                    ]),
                    QuoteBlock(children=[
                        PlainInline(text='マークダウンとは')
                    ]),
                    QuoteBlock(children=[
                        PlainInline(text='これです')
                    ])
                ]),
                [
                    [
                        HeadingBlock(size=1, children=[
                            PlainInline(text='マークダウンとは')
                        ])
                    ],
                    [
                        QuoteBlock(children=[
                            PlainInline(text='マークダウンとは')
                        ]),
                        QuoteBlock(children=[
                            PlainInline(text='これです')
                        ])
                    ]
                ]
            ),

            (
                ParseResult(content=[
                    QuoteBlock(children=[
                        PlainInline(text='昨日私はこう言いました')
                    ]),
                    ParagraphBlock(indent_depth=0, children=[
                        PlainInline(text='一日が過ぎました')
                    ]),
                    QuoteBlock(children=[
                        PlainInline(text='今日私はこう言いました')
                    ]),
                    QuoteBlock(children=[
                        PlainInline(text='帰りたい')
                    ]),
                ]),
                [
                    [
                        QuoteBlock(children=[
                            PlainInline(text='昨日私はこう言いました')
                        ])
                    ],
                    [
                        ParagraphBlock(indent_depth=0, children=[
                            PlainInline(text='一日が過ぎました')
                        ])
                    ],
                    [
                        QuoteBlock(children=[
                            PlainInline(text='今日私はこう言いました')
                        ]),
                        QuoteBlock(children=[
                            PlainInline(text='帰りたい')
                        ]),
                    ]
                ]
            ),
        ],
        ids=['two type', 'two type between']
    )
    def test_multiple_type_blocks(self, parse_result: ParseResult, expected_list_of_list: list[list[Block]]):
        # GIVEN
        sut = split_to_convert_target

        # WHEN
        for convert_target, expected_list in zip(sut(parse_result.content), expected_list_of_list):
            # THEN
            assert_same_block_list(convert_target, expected_list)
