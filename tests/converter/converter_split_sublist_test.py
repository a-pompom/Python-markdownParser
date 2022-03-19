import pytest

from a_pompom_markdown_parser.converter.converter import split_to_convert_target
from a_pompom_markdown_parser.markdown.parser import MarkdownParser
from a_pompom_markdown_parser.element.block import Block, ParagraphBlock, QuoteBlock, HeadingBlock
from a_pompom_markdown_parser.element.inline import PlainInline


# blockのリスト同士が同一とみなせるか判定
def assert_same_block_list(actual_list: list[Block], expected_list: list[Block]):
    for actual, expected in zip(actual_list, expected_list):
        assert actual == expected


class TestSplitToConvertTarget:
    """ コンバータで処理できるようBlockのリストを種別ごとに分割 """

    # 1種類のBlock要素のみで構成
    @pytest.mark.parametrize(
        ('lines', 'expected_list_of_list'),
        [
            (
                ['first plain text', 'second plain text'],
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
                ['> 私は昨日', '> こう言いました'],
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
        ],
        ids=['only plain', 'only block quote']
    )
    def test_only_single_type_block(self, lines: list[str], expected_list_of_list: list[list[Block]]):
        # GIVEN
        sut = split_to_convert_target
        blocks = MarkdownParser().parse(lines).content

        # WHEN
        for convert_target, expected_list in zip(sut(blocks), expected_list_of_list):
            # THEN
            assert_same_block_list(convert_target, expected_list)

    # 複数の種類のBlock要素が混在
    @pytest.mark.parametrize(
        ('lines', 'expected_list_of_list'),
        [
            (
                ['# マークダウンとは', '> マークダウンとは', '> これです'],
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
                ['> 昨日私はこう言いました', '一日が過ぎました', '> 今日私はこう言いました', '> 帰りたい'],
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
    def test_multiple_type_blocks(self, lines: list[str], expected_list_of_list: list[list[Block]]):
        # GIVEN
        sut = split_to_convert_target
        blocks = MarkdownParser().parse(lines).content

        # WHEN
        for convert_target, expected_list in zip(sut(blocks), expected_list_of_list):
            # THEN
            assert_same_block_list(convert_target, expected_list)
