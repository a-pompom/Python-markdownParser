import pytest

from a_pompom_markdown_parser.converter.converter import Converter
from a_pompom_markdown_parser.element.block import ParseResult, QuoteBlock, ParagraphBlock, HeadingBlock, CodeBlock, \
    PlainBlock
from a_pompom_markdown_parser.element.inline import PlainInline
from a_pompom_markdown_parser.markdown.parser import MarkdownParser


class TestConverter:
    """ 複数行に渡る処理を統合、といったマークダウンとHTMLの橋渡し処理を検証 """

    # 変換の無いものはそのまま出力されるか
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (
                ['# 概要', 'これは概要です。'],
                ParseResult(content=[
                    HeadingBlock(size=1, children=[
                        PlainInline(text='概要')
                    ]),
                    ParagraphBlock(indent_depth=0, children=[
                        PlainInline(text='これは概要です。')
                    ])
                ])
            ),
        ]
    )
    def test_no_convert(self, lines: list[str], expected: ParseResult):
        # GIVEN
        sut = Converter()
        markdown_result = MarkdownParser().parse(lines)
        # WHEN
        actual = sut.convert(markdown_result)
        # THEN
        assert actual == expected

    # 要素を1つに統合できるか
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (
                ['> いい感じのことを', '> 言っているようです'],
                ParseResult(content=[
                    QuoteBlock(children=[
                        ParagraphBlock(indent_depth=1, children=[
                            PlainInline(text='いい感じのことを')
                        ]),
                        ParagraphBlock(indent_depth=1, children=[
                            PlainInline(text='言っているようです')
                        ])
                    ])
                ])
            ),

            (
                ['## Pythonとは', '> Pythonとは', '> プログラミング言語です', '小休止', '> 再開'],
                ParseResult(content=[
                    HeadingBlock(size=2, children=[
                        PlainInline(text='Pythonとは')
                    ]),
                    QuoteBlock(children=[
                        ParagraphBlock(indent_depth=1, children=[
                            PlainInline(text='Pythonとは')
                        ]),
                        ParagraphBlock(indent_depth=1, children=[
                            PlainInline(text='プログラミング言語です')
                        ]),
                    ]),
                    ParagraphBlock(indent_depth=0, children=[
                        PlainInline(text='小休止')
                    ]),
                    QuoteBlock(children=[
                        ParagraphBlock(indent_depth=1, children=[
                            PlainInline(text='再開')
                        ])
                    ])
                ])
            )

        ],
        ids=['only one type element', 'mixed']
    )
    def test_convert(self, lines: list[str], expected: ParseResult):
        # GIVEN
        sut = Converter()
        markdown_result = MarkdownParser().parse(lines)
        # WHEN
        actual = sut.convert(markdown_result)
        # THEN
        assert actual == expected

    # コードブロック要素の範囲内を1つに統合できるか
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (
                ['```Python', '# comment, not heading', 'def func():', '```'],
                ParseResult(content=[
                    CodeBlock(language='Python', children=[
                        PlainBlock(indent_depth=0, children=[
                            PlainInline(text='# comment, not heading')
                        ]),
                        PlainBlock(indent_depth=0, children=[
                            PlainInline(text='def func():')
                        ]),
                    ])
                ])
            ),

            (
                ['```', '[参考](https://)', '> コードは終わっていたはずです'],
                ParseResult(content=[
                    CodeBlock(language='', children=[
                        PlainBlock(indent_depth=0, children=[
                            PlainInline(text='[参考](https://)')
                        ]),
                        PlainBlock(indent_depth=0, children=[
                            PlainInline(text='> コードは終わっていたはずです')
                        ]),
                    ])
                ])
            ),
        ],
        ids=['has end', 'no end']
    )
    def test_convert_code_block(self, lines: list[str], expected: ParseResult):
        # GIVEN
        sut = Converter()
        markdown_result = MarkdownParser().parse(lines)
        # WHEN
        actual = sut.convert(markdown_result)
        # THEN
        assert actual == expected
