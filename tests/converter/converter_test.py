import pytest

from a_pompom_markdown_parser.converter.converter import Converter
from a_pompom_markdown_parser.element.block import ParseResult, QuoteBlock, ParagraphBlock, HeadingBlock, CodeBlock, \
    PlainBlock, ListBlock, ListItemBlock, TableOfContentsBlock, CodeChildBlock
from a_pompom_markdown_parser.element.inline import PlainInline, LinkInline


class TestConverter:
    """ 複数行に渡る処理を統合、といったマークダウンとHTMLの橋渡し処理を検証 """

    # 変換の無いものはそのまま出力されるか
    @pytest.mark.parametrize(
        ('parse_result', 'expected'),
        [
            (
                ParseResult(content=[
                    HeadingBlock(size=1, children=[
                        PlainInline(text='概要')
                    ]),
                    ParagraphBlock(indent_depth=0, children=[
                        PlainInline(text='これは概要です。')
                    ])
                ]),
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
    def test_no_convert(self, parse_result: ParseResult, expected: ParseResult):
        # GIVEN
        sut = Converter()
        # WHEN
        actual = sut.convert(parse_result)
        # THEN
        assert actual == expected

    # 要素を1つに統合できるか
    @pytest.mark.parametrize(
        ('parse_result', 'expected'),
        [
            (
                ParseResult(content=[
                    QuoteBlock(children=[
                        PlainInline(text='いい感じのことを')
                    ]),
                    QuoteBlock(children=[
                        PlainInline(text='言っているようです')
                    ]),
                ]),
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
                ParseResult(content=[
                    HeadingBlock(size=2, children=[
                        PlainInline(text='Pythonとは')
                    ]),
                    QuoteBlock(children=[
                        PlainInline(text='Pythonとは')
                    ]),
                    QuoteBlock(children=[
                        PlainInline(text='プログラミング言語です')
                    ]),
                    ParagraphBlock(indent_depth=0, children=[
                        PlainInline(text='小休止')
                    ]),
                    QuoteBlock(children=[
                        PlainInline(text='再開')
                    ]),
                ]),

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
    def test_convert(self, parse_result: ParseResult, expected: ParseResult):
        # GIVEN
        sut = Converter()
        # WHEN
        actual = sut.convert(parse_result)
        # THEN
        assert actual == expected

    # コードブロック要素の範囲内を1つに統合できるか
    @pytest.mark.parametrize(
        ('parse_result', 'expected'),
        [
            (
                ParseResult(content=[
                    CodeBlock(language='Python', children=[]),
                    CodeChildBlock(children=[
                        PlainInline(text='# comment, not heading')
                    ]),
                    CodeChildBlock(children=[
                        PlainInline(text='def func():')
                    ]),
                ]),
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
                ParseResult(content=[
                    CodeBlock(language='', children=[]),
                    CodeChildBlock(children=[
                        PlainInline(text='[参考](https://)')
                    ]),
                    CodeChildBlock(children=[
                        PlainInline(text='> コードは終わっていたはずです')
                    ]),
                ]),
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
    def test_convert_code_block(self, parse_result: ParseResult, expected: ParseResult):
        # GIVEN
        sut = Converter()
        # WHEN
        actual = sut.convert(parse_result)
        # THEN
        assert actual == expected

    # 目次を表現するBlockをul/li Blockへ変換できるか
    @pytest.mark.parametrize(
        ('parse_result', 'expected'),
        [
            (
                ParseResult(content=[
                    HeadingBlock(size=1, children=[
                        PlainInline(text='概要')
                    ]),
                    TableOfContentsBlock(children=[
                        PlainInline(text='')
                    ]),
                    ParagraphBlock(indent_depth=0, children=[
                        PlainInline(text='概要を書きます')
                    ]),
                    HeadingBlock(size=2, children=[
                        LinkInline(href='表示されないテキスト', text='リンクを含むヘッダです')
                    ]),
                    HeadingBlock(size=1, children=[
                        PlainInline(text='新たな概要です')
                    ]),
                    HeadingBlock(size=3, children=[
                        PlainInline(text='補足しておきます')
                    ])
                ]),
                ParseResult(content=[
                    HeadingBlock(size=1, children=[
                        PlainInline(text='概要')
                    ]),
                    ListBlock(indent_depth=0, children=[
                        ListItemBlock(indent_depth=1, children=[
                            LinkInline(href='#概要', text='概要')
                        ]),
                        ListItemBlock(indent_depth=1, children=[
                            ListBlock(indent_depth=2, children=[
                                ListItemBlock(indent_depth=3, children=[
                                    LinkInline(href='#リンクを含むヘッダです', text='リンクを含むヘッダです')
                                ])
                            ])
                        ])
                    ]),
                    ListBlock(indent_depth=0, children=[
                        ListItemBlock(indent_depth=1, children=[
                            LinkInline(href='#新たな概要です', text='新たな概要です')
                        ]),
                        ListItemBlock(indent_depth=1, children=[
                            ListBlock(indent_depth=2, children=[
                                ListItemBlock(indent_depth=3, children=[
                                    LinkInline(href='#補足しておきます', text='補足しておきます')
                                ])
                            ])
                        ])
                    ]),
                    ParagraphBlock(indent_depth=0, children=[
                        PlainInline(text='概要を書きます')
                    ]),
                    HeadingBlock(size=2, children=[
                        LinkInline(href='表示されないテキスト', text='リンクを含むヘッダです')
                    ]),
                    HeadingBlock(size=1, children=[
                        PlainInline(text='新たな概要です')
                    ]),
                    HeadingBlock(size=3, children=[
                        PlainInline(text='補足しておきます')
                    ])
                ])
            )
        ]
    )
    def test_convert_toc(self, parse_result: ParseResult, expected: ParseResult):
        # GIVEN
        sut = Converter()
        # WHEN
        actual = sut.convert(parse_result)
        # THEN
        assert actual == expected
