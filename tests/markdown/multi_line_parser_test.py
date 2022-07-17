import pytest

from a_pompom_markdown_parser.element.block import Block, CodeBlock, CodeChildBlock
from a_pompom_markdown_parser.element.inline import PlainInline
from a_pompom_markdown_parser.markdown.multi_line_parser import MultiLineParser, CodeBlockParser


class TestMultiLineParser:
    """ 複数行にわたるマークダウン記法を解釈できるか """

    # 記法は処理対象か
    @pytest.mark.parametrize(
        ('line', 'expected'),
        [
            ('# おはよう', False),
            ('```Python', True),
            ('```', True),
        ]
    )
    def test_is_target(self, line: str, expected: bool):
        # GIVEN
        sut = MultiLineParser()
        # WHEN
        actual = sut.is_target(line)
        # THEN
        assert actual == expected

    # 記法を含む範囲を解釈できるか
    @pytest.mark.parametrize(
        ('lines', 'expected_block_list', 'expected_length'),
        [
            (
                ['```Python', 'print(0)', '```'],
                [
                    CodeBlock(language='Python', children=[]),
                    CodeChildBlock(children=[PlainInline(text='print(0)')])
                ],
                2
            ),
            (
                ['```JavaScript', '// コメントしておきます'],
                [
                    CodeBlock(language='JavaScript', children=[]),
                    CodeChildBlock(children=[PlainInline(text='// コメントしておきます')])
                ],
                2
            ),
        ]
    )
    def test_parse(self, lines: list[str], expected_block_list: list[Block], expected_length: int):
        # GIVEN
        sut = MultiLineParser()
        # WHEN
        actual_list, actual_length = sut.parse(lines)
        # THEN
        assert actual_length == expected_length
        for actual, expected in zip(actual_list, expected_block_list):
            assert actual == expected


class TestCodeBlockParser:
    """ 複数行にわたるコードブロックを解釈できるか """

    # コードブロックの開始要素を判別できるか
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            ('```Python', True),
            ('``', False),
            ('not code block', False)
        ]
    )
    def test_is_target(self, text: str, expected: bool):
        # GIVEN
        sut = CodeBlockParser()
        # WHEN
        actual = sut.is_target(text)
        # THEN
        assert actual == expected

    # コードブロックの範囲を抽出できるか
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (
                ['```HTML', '<h1>Hello</h1>', '```'],
                2
            ),
            (
                ['```Python', '# comment'],
                2
            ),
            (
                ['```'],
                1
            ),
        ]
    )
    def test_extract_parse_range(self, lines: list[str], expected: int):
        # GIVEN
        sut = CodeBlockParser()
        # WHEN
        actual = sut.extract_parse_range(lines)
        # THEN
        assert actual == expected

    # 記法を解釈できるか
    @pytest.mark.parametrize(
        ('code_lines', 'expected_list'),
        [
            (
                ['```Python', '# コメントです', '```'],
                [
                    CodeBlock(language='Python', children=[]),
                    CodeChildBlock(children=[PlainInline(text='# コメントです')])
                ]
            ),
            (
                ['```JavaScript', 'const message = "Hello";', 'console.log(message);'],
                [
                    CodeBlock(language='JavaScript', children=[]),
                    CodeChildBlock(children=[PlainInline(text='const message = "Hello";')]),
                    CodeChildBlock(children=[PlainInline(text='console.log(message);')]),
                ]
            ),
        ]
    )
    def test_parse(self, code_lines: list[str], expected_list: list[Block]):
        # GIVEN
        sut = CodeBlockParser()
        # WHEN
        actual_list = sut.parse(code_lines)
        # THEN
        for actual, expected in zip(actual_list, expected_list):
            assert actual == expected
