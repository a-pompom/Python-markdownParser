import pytest

from a_pompom_markdown_parser.converter.converter import group_same_range_blocks
from a_pompom_markdown_parser.markdown.parser import MarkdownParser


class TestGrouping:
    """ 同範囲を同一とみなすBlock要素をグルーピングできるか"""

    # CodeBlockの範囲内では当該メソッドによりCodeBlockへグループ化されるか
    @pytest.mark.parametrize(
        ('lines', 'expected_list'),
        [
            (
                ['```JavaScript', 'const i = 0;', '```', 'plain text'],
                ['[CodeBlock: language=JavaScript | Child of CodeBlock -> Plain: text=]',
                 '[CodeChildBlock: | Child of CodeChildBlock -> Plain: text=const i = 0;]',
                 '[Paragraph: indent_depth=0 | Child of Paragraph -> Plain: text=plain text]']
            ),
            (
                ['# heading', '```', 'sort();', '```'],
                ['[Heading: size=1 | Child of Heading -> Plain: text=heading]',
                 '[CodeBlock: language= | Child of CodeBlock -> Plain: text=]',
                 '[CodeChildBlock: | Child of CodeChildBlock -> Plain: text=sort();]']
            ),
            (
                ['本文', '```python', 'for (int i=0; i < 10; i++)', '```'],
                ['[Paragraph: indent_depth=0 | Child of Paragraph -> Plain: text=本文]',
                 '[CodeBlock: language=python | Child of CodeBlock -> Plain: text=]',
                 '[CodeChildBlock: | Child of CodeChildBlock -> Plain: text=for (int i=0; i < 10; i++)]']

            ),
            (
                ['コードの例を示します。', '```', '> 入れ忘れました'],
                ['[Paragraph: indent_depth=0 | Child of Paragraph -> Plain: text=コードの例を示します。]',
                 '[CodeBlock: language= | Child of CodeBlock -> Plain: text=]',
                 '[CodeChildBlock: | Child of CodeChildBlock -> Plain: text=> 入れ忘れました]']
            ),
        ],
        ids=['head', 'between', 'tail', 'no end']
    )
    def test_code_block(self, lines: list[str], expected_list: list[str]):
        # GIVEN
        sut = group_same_range_blocks
        blocks = MarkdownParser().parse(lines).content
        # WHEN
        actual_blocks = sut(blocks)

        # THEN
        for actual, expected in zip(actual_blocks, expected_list):
            assert repr(actual) == expected

    # グループ化対象外のものはそのまま出力されるか
    @pytest.mark.parametrize(
        ('lines', 'expected_list'),
        [
            (
                ['plain text', '# heading'],
                ['[Paragraph: indent_depth=0 | Child of Paragraph -> Plain: text=plain text]',
                 '[Heading: size=1 | Child of Heading -> Plain: text=heading]']
            )
        ]
    )
    def test_not_grouping(self, lines: list[str], expected_list: list[str]):
        # GIVEN
        sut = group_same_range_blocks
        blocks = MarkdownParser().parse(lines).content
        # WHEN
        actual_blocks = sut(blocks)

        # THEN
        for actual, expected in zip(actual_blocks, expected_list):
            assert repr(actual) == expected
