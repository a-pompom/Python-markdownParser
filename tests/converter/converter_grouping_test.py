import pytest

from a_pompom_markdown_parser.converter.converter import group_same_range_blocks
from a_pompom_markdown_parser.element.block import Block, CodeBlock, CodeChildBlock, ParagraphBlock, HeadingBlock
from a_pompom_markdown_parser.element.inline import PlainInline
from a_pompom_markdown_parser.markdown.parser import MarkdownParser


class TestGrouping:
    """ 同範囲を同一とみなすBlock要素をグルーピングできるか"""

    # CodeBlockの範囲内では当該メソッドによりCodeBlockへグループ化されるか
    @pytest.mark.parametrize(
        ('lines', 'expected_list'),
        [
            (
                ['```JavaScript', 'const i = 0;', '```', 'plain text'],
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
                ['# heading', '```', 'sort();', '```'],
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
                ['本文', '```python', 'for (int i=0; i < 10; i++)', '```'],
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
                ['コードの例を示します。', '```', '> 入れ忘れました'],
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
    def test_code_block(self, lines: list[str], expected_list: list[Block]):
        # GIVEN
        sut = group_same_range_blocks
        blocks = MarkdownParser().parse(lines).content
        # WHEN
        actual_blocks = sut(blocks)

        # THEN
        for actual, expected in zip(actual_blocks, expected_list):
            assert actual == expected

    # グループ化対象外のものはそのまま出力されるか
    @pytest.mark.parametrize(
        ('lines', 'expected_list'),
        [
            (
                ['plain text', '# heading'],
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
    def test_not_grouping(self, lines: list[str], expected_list: list[Block]):
        # GIVEN
        sut = group_same_range_blocks
        blocks = MarkdownParser().parse(lines).content
        # WHEN
        actual_blocks = sut(blocks)

        # THEN
        for actual, expected in zip(actual_blocks, expected_list):
            assert actual == expected
