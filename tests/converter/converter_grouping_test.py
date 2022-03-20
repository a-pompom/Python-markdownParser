import pytest

from a_pompom_markdown_parser.converter.converter import group_same_range_blocks
from a_pompom_markdown_parser.element.block import Block, CodeBlock, CodeChildBlock, ParagraphBlock, HeadingBlock, \
    ParseResult, PlainBlock
from a_pompom_markdown_parser.element.inline import PlainInline


class TestGrouping:
    """ 同範囲を同一とみなすBlock要素をグルーピングできるか"""

    # CodeBlockの範囲内では当該メソッドによりCodeBlockへグループ化されるか
    @pytest.mark.parametrize(
        ('parse_result', 'expected_list'),
        [
            (
                ParseResult(content=[
                    CodeBlock(language='JavaScript', children=[
                        PlainInline(text='')
                    ]),
                    PlainBlock(indent_depth=0, children=[
                        PlainInline(text='const i = 0;')
                    ]),
                    CodeBlock(language='', children=[
                        PlainInline(text='')
                    ]),
                    ParagraphBlock(indent_depth=0, children=[
                        PlainInline(text='plain text')
                    ])
                ]),
                [
                    CodeBlock(language='JavaScript', children=[
                        PlainInline(text='')
                    ]),
                    CodeChildBlock(children=[
                        PlainInline(text='const i = 0;')
                    ]),
                    ParagraphBlock(indent_depth=0, children=[
                        PlainInline(text='plain text')
                    ])
                ]
            ),
            (
                ParseResult(content=[
                    HeadingBlock(size=1, children=[
                        PlainInline(text='heading')
                    ]),
                    CodeBlock(language='', children=[
                        PlainInline(text='')
                    ]),
                    PlainBlock(indent_depth=0, children=[
                        PlainInline(text='sort();')
                    ]),
                    CodeBlock(language='', children=[
                        PlainInline(text='')
                    ]),
                ]),
                [
                    HeadingBlock(size=1, children=[
                        PlainInline(text='heading')
                    ]),
                    CodeBlock(language='', children=[
                        PlainInline(text='')
                    ]),
                    CodeChildBlock(children=[
                        PlainInline(text='sort();')
                    ])
                ]
            ),
            (
                ParseResult(content=[
                    ParagraphBlock(indent_depth=0, children=[
                        PlainInline(text='本文')
                    ]),
                    CodeBlock(language='python', children=[
                        PlainInline(text='')
                    ]),
                    PlainBlock(indent_depth=0, children=[
                        PlainInline(text='for (int i=0; i < 10; i++)')
                    ]),
                    CodeBlock(language='', children=[
                        PlainInline(text='')
                    ]),
                ]),
                [
                    ParagraphBlock(indent_depth=0, children=[
                        PlainInline(text='本文')
                    ]),
                    CodeBlock(language='python', children=[
                        PlainInline(text='')
                    ]),
                    CodeChildBlock(children=[
                        PlainInline(text='for (int i=0; i < 10; i++)')
                    ])
                ]
            ),
            (
                ParseResult(content=[
                    ParagraphBlock(indent_depth=0, children=[
                        PlainInline(text='コードの例を示します。')
                    ]),
                    CodeBlock(language='', children=[
                        PlainInline(text='')
                    ]),
                    PlainBlock(indent_depth=0, children=[
                        PlainInline(text='> 入れ忘れました')
                    ]),
                ]),
                [
                    ParagraphBlock(indent_depth=0, children=[
                        PlainInline(text='コードの例を示します。')
                    ]),
                    CodeBlock(language='', children=[
                        PlainInline(text='')
                    ]),
                    CodeChildBlock(children=[
                        PlainInline(text='> 入れ忘れました')
                    ])
                ]
            ),
        ],
        ids=['head', 'between', 'tail', 'no end']
    )
    def test_code_block(self, parse_result: ParseResult, expected_list: list[Block]):
        # GIVEN
        sut = group_same_range_blocks
        # WHEN
        actual_blocks = sut(parse_result.content)

        # THEN
        for actual, expected in zip(actual_blocks, expected_list):
            assert actual == expected

    # グループ化対象外のものはそのまま出力されるか
    @pytest.mark.parametrize(
        ('parse_result', 'expected_list'),
        [
            (
                ParseResult(content=[
                    ParagraphBlock(indent_depth=0, children=[
                        PlainInline(text='plain text')
                    ]),
                    HeadingBlock(size=1, children=[
                        PlainInline(text='heading')
                    ]),
                ]),
                [
                    ParagraphBlock(indent_depth=0, children=[
                        PlainInline(text='plain text')
                    ]),
                    HeadingBlock(size=1, children=[
                        PlainInline(text='heading')
                    ])
                ]
            )
        ]
    )
    def test_not_grouping(self, parse_result: ParseResult, expected_list: list[Block]):
        # GIVEN
        sut = group_same_range_blocks
        # WHEN
        actual_blocks = sut(parse_result.content)

        # THEN
        for actual, expected in zip(actual_blocks, expected_list):
            assert actual == expected
