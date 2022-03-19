import pytest

from a_pompom_markdown_parser.element.block import ParseResult, ParagraphBlock, HeadingBlock, QuoteBlock, ListBlock, \
    HorizontalRuleBlock, CodeBlock, PlainBlock
from a_pompom_markdown_parser.element.inline import PlainInline, LinkInline, CodeInline, ImageInline
from a_pompom_markdown_parser.markdown.parser import MarkdownParser


class TestMarkdownParser:
    """ Block/Inlineをまとめて扱い、行文字列からマークダウンのパース結果を生成する機能を検証 """

    # パース結果
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (
                ['plain text'],
                ParseResult(content=[
                    ParagraphBlock(indent_depth=0, children=[
                        PlainInline(text='plain text')
                    ])
                ])
            ),

            (
                ['## awesome heading'],
                ParseResult(content=[
                    HeadingBlock(size=2, children=[
                        PlainInline(text='awesome heading')
                    ])
                ])
            ),

            (
                ['> amazing quote text'],
                ParseResult(content=[
                    QuoteBlock(children=[
                        PlainInline(text='amazing quote text')
                    ])
                ])
            ),

            (
                ['* 1st element', '* 2nd element'],
                ParseResult(content=[
                    ListBlock(indent_depth=0, children=[
                        PlainInline(text='1st element')
                    ]),
                    ListBlock(indent_depth=0, children=[
                        PlainInline(text='2nd element')
                    ])
                ])
            ),

            (
                ['---'],
                ParseResult(content=[
                    HorizontalRuleBlock(children=[
                        PlainInline(text='')
                    ])
                ])
            ),
        ],
        ids=['plain', 'heading', 'quote', 'list', 'horizontal rule'])
    def test_parse_block(self, lines: list[str], expected: ParseResult):
        # GIVEN
        sut = MarkdownParser()
        # WHEN
        actual = sut.parse(lines)
        # THEN
        assert actual == expected

    # Inline要素をパースできるか
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (
                ['[公式](https://docs.python.org/3/)を参照'],
                ParseResult(content=[
                    ParagraphBlock(indent_depth=0, children=[
                        LinkInline(href='https://docs.python.org/3/', text='公式'),
                        PlainInline(text='を参照')
                    ])
                ])
            ),

            (
                ['記号`!`は否定を表現します。'],
                ParseResult(content=[
                    ParagraphBlock(indent_depth=0, children=[
                        PlainInline(text='記号'),
                        CodeInline(text='!'),
                        PlainInline(text='は否定を表現します。')
                    ])
                ])
            ),

            (
                ['![image](https://avatars.githubusercontent.com/u/43694794?v=4)'],
                ParseResult(content=[
                    ParagraphBlock(indent_depth=0, children=[
                        ImageInline(src='https://avatars.githubusercontent.com/u/43694794?v=4', alt='image', text='')
                    ])
                ])
            ),
        ],
        ids=['link', 'code', 'image']
    )
    def test_parse_inline(self, lines: list[str], expected: ParseResult):
        # GIVEN
        sut = MarkdownParser()
        # WHEN
        actual = sut.parse(lines)
        # THEN
        assert actual == expected

    # Block/Inline要素が混在した行をパースできるか
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (
                [
                    '## [Google](https://www.google.com/)とは',
                    '> `Google`の概要',
                ],
                ParseResult(content=[
                    HeadingBlock(size=2, children=[
                        LinkInline(href='https://www.google.com/', text='Google'),
                        PlainInline(text='とは')
                    ]),
                    QuoteBlock(children=[
                        CodeInline(text='Google'),
                        PlainInline(text='の概要')
                    ])
                ])
            )
        ]
    )
    def test_parse_mixed(self, lines: list[str], expected: ParseResult):
        # GIVEN
        sut = MarkdownParser()
        # WHEN
        actual = sut.parse(lines)
        # THEN
        assert actual == expected

    # コードブロックのモードを制御できているか
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (
                ['## 概要', '> すてきな概要です'],
                ParseResult(content=[
                    HeadingBlock(size=2, children=[
                        PlainInline(text='概要')
                    ]),
                    QuoteBlock(children=[
                        PlainInline(text='すてきな概要です')
                    ])
                ])
            ),

            (
                ['### サンプルコード', '```Python', '# Pythonのコメント', '```', '#### 上はサンプルコードです'],
                ParseResult(content=[
                    HeadingBlock(size=3, children=[
                        PlainInline(text='サンプルコード')
                    ]),
                    CodeBlock(language='Python', children=[
                        PlainInline(text='')
                    ]),
                    PlainBlock(children=[
                        PlainInline(text='# Pythonのコメント')
                    ]),
                    CodeBlock(language='', children=[
                        PlainInline(text='')
                    ]),
                    HeadingBlock(size=4, children=[
                        PlainInline(text='上はサンプルコードです')
                    ])
                ])
            ),

            (
                ['> コードが始まります', '```', '## コードを閉じるのを忘れました', '[まだコードです](url)'],
                ParseResult(content=[
                    QuoteBlock(children=[
                        PlainInline(text='コードが始まります')
                    ]),
                    CodeBlock(language='', children=[
                        PlainInline(text='')
                    ]),
                    PlainBlock(indent_depth=0, children=[
                        PlainInline(text='## コードを閉じるのを忘れました')
                    ]),
                    PlainBlock(indent_depth=0, children=[
                        PlainInline(text='[まだコードです](url)')
                    ]),
                ])
            ),
        ],
        ids=['no code block', 'code block with end symbol', 'no end symbol']
    )
    def test_parse_code_block_mode(self, lines: list[str], expected: ParseResult):
        # GIVEN
        sut = MarkdownParser()
        # WHEN
        actual = sut.parse(lines)
        # THEN
        assert actual == expected
