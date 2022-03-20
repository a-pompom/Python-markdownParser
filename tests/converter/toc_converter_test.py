import pytest

from a_pompom_markdown_parser.element.block import HeadingBlock, ListBlock, ListItemBlock, ParseResult, ParagraphBlock
from a_pompom_markdown_parser.element.inline import LinkInline, PlainInline
from a_pompom_markdown_parser.converter.toc_converter import TocNodeTreeGenerator, TocNode, TocGenerator, TocConverter
from a_pompom_markdown_parser.markdown.parser import MarkdownParser


class TestTocNodeTreeGenerator:
    """ ヘッダBlockから目次構造のツリーをつくれるか検証 """

    # ヘッダから対応する目次構造のツリーをつくれるか
    @pytest.mark.parametrize(
        ('header_text_list', 'expected_list'),
        [
            (
                ['# 概要'],
                [TocNode(depth=1, text='概要', children=[])]
            ),
            (
                ['# 概要', '## ゴール'],
                [TocNode(depth=1, text='概要', children=[
                    TocNode(depth=2, text='ゴール', children=[])])
                 ]
            ),
            (
                ['# 概要', '## 用語整理', '### Pythonとは', '#### 補足: Pythonの由来', '### たのしいPython'],
                [TocNode(depth=1, text='概要', children=[
                    TocNode(depth=2, text='用語整理', children=[
                        TocNode(depth=3, text='Pythonとは', children=[
                            TocNode(depth=4, text='補足: Pythonの由来', children=[])
                        ])
                        , TocNode(depth=3, text='たのしいPython', children=[])
                    ])
                ])]
            ),
            (
                ['# 目次の`テスト`', '## [link](url)'],
                [TocNode(depth=1, text='目次のテスト', children=[
                    TocNode(depth=2, text='link', children=[])
                ])]
            )
        ],
        ids=['single element', 'single child', 'multiple child', 'contains inline element']
    )
    def test_generate_single_tree(self, header_text_list: list[str], expected_list: list[TocNode]):
        # GIVEN
        sut = TocNodeTreeGenerator()
        block_list = MarkdownParser().parse(header_text_list).content
        header_list = [block for block in block_list if isinstance(block, HeadingBlock)]

        # WHEN
        actual_list = sut.generate(header_list)
        # THEN
        for actual, expected in zip(actual_list, expected_list):
            assert actual == expected

    # 複数の木で表現される目次をつくれるか
    @pytest.mark.parametrize(
        ('header_text_list', 'expected_list'),
        [
            (
                ['## 今日やること', '## 明日やること'],
                [
                    TocNode(depth=2, text='今日やること', children=[]),
                    TocNode(depth=2, text='明日やること', children=[]),
                ]
            ),
            (
                ['## カレーのつくりかた', '### 材料', '### 手順', '#### 切る', '#### 煮込む', '### 仕上げ',
                 '## 冷奴のつくりかた', '### 材料', '#### おわり'],
                [
                    TocNode(depth=2, text='カレーのつくりかた', children=[
                        TocNode(depth=3, text='材料', children=[]),
                        TocNode(depth=3, text='手順', children=[
                            TocNode(depth=4, text='切る', children=[]),
                            TocNode(depth=4, text='煮込む', children=[]),
                        ]),
                        TocNode(depth=3, text='仕上げ', children=[])
                    ]),
                    TocNode(depth=2, text='冷奴のつくりかた', children=[
                        TocNode(depth=3, text='材料', children=[
                            TocNode(depth=4, text='おわり', children=[])
                        ])
                    ])
                ]
            )
        ]
    )
    def test_generate_multiple_trees(self, header_text_list: list[str], expected_list: list[TocNode]):
        # GIVEN
        sut = TocNodeTreeGenerator()
        block_list = MarkdownParser().parse(header_text_list).content
        header_list = [block for block in block_list if isinstance(block, HeadingBlock)]

        # WHEN
        actual_list = sut.generate(header_list)
        # THEN
        for actual, expected in zip(actual_list, expected_list):
            assert actual == expected


class TestTocGenerator:
    """ TocNodeからul liで表現される目次Blockをつくれるか検証 """

    # 単一の目次の木を組み立てられるか
    @pytest.mark.parametrize(
        ('toc_node_list', 'expected_list'),
        [
            (
                [
                    TocNode(depth=1, text='概要', children=[])
                ],
                [
                    ListBlock(indent_depth=0, children=[
                        ListItemBlock(indent_depth=1, children=[
                            LinkInline(href='#概要', text='概要')
                        ])
                    ])
                ]
            ),

            (
                [
                    TocNode(depth=1, text='概要', children=[
                        TocNode(depth=2, text='ゴール', children=[]),
                        TocNode(depth=2, text='用語整理', children=[])
                    ])
                ],
                [
                    ListBlock(indent_depth=0, children=[
                        ListItemBlock(indent_depth=1, children=[
                            LinkInline(href='#概要', text='概要')
                        ]),
                        ListItemBlock(indent_depth=1, children=[
                            ListBlock(indent_depth=2, children=[
                                ListItemBlock(indent_depth=3, children=[
                                    LinkInline(href='#ゴール', text='ゴール')
                                ]),
                                ListItemBlock(indent_depth=3, children=[
                                    LinkInline(href='#用語整理', text='用語整理')
                                ]),
                            ])
                        ])
                    ])
                ]
            ),

            (
                [TocNode(depth=1, text='はじめに', children=[
                    TocNode(depth=2, text='Pythonとは', children=[
                        TocNode(depth=3, text='なぜPythonなのか', children=[]),
                        TocNode(depth=3, text='どうしてPythonなのか', children=[])
                    ]),
                    TocNode(depth=2, text='Djangoとは', children=[
                        TocNode(depth=3, text='なぜDjangoなのか', children=[
                            TocNode(depth=4, text='ゆえにDjangoである', children=[])
                        ])
                    ])
                ])],
                [
                    ListBlock(indent_depth=0, children=[
                        ListItemBlock(indent_depth=1, children=[
                            LinkInline(href='#はじめに', text='はじめに')
                        ]),
                        ListItemBlock(indent_depth=1, children=[
                            ListBlock(indent_depth=2, children=[
                                ListItemBlock(indent_depth=3, children=[
                                    LinkInline(href='#Pythonとは', text='Pythonとは')
                                ]),
                                ListItemBlock(indent_depth=3, children=[
                                    ListBlock(indent_depth=4, children=[
                                        ListItemBlock(indent_depth=5, children=[
                                            LinkInline(href='#なぜPythonなのか', text='なぜPythonなのか')
                                        ]),
                                        ListItemBlock(indent_depth=5, children=[
                                            LinkInline(href='#どうしてPythonなのか', text='どうしてPythonなのか')
                                        ])
                                    ])
                                ]),
                                ListItemBlock(indent_depth=3, children=[
                                    LinkInline(href='#Djangoとは', text='Djangoとは')
                                ]),
                                ListItemBlock(indent_depth=3, children=[
                                    ListBlock(indent_depth=4, children=[
                                        ListItemBlock(indent_depth=5, children=[
                                            LinkInline(href='#なぜDjangoなのか', text='なぜDjangoなのか')
                                        ]),
                                        ListItemBlock(indent_depth=5, children=[
                                            ListBlock(indent_depth=6, children=[
                                                ListItemBlock(indent_depth=7, children=[
                                                    LinkInline(href='#ゆえにDjangoである', text='ゆえにDjangoである')
                                                ])
                                            ])
                                        ])
                                    ])
                                ])
                            ])
                        ]),
                    ])
                ],
            )
        ]
    )
    def test_single_node(self, toc_node_list: list[TocNode], expected_list: list[ListBlock]):
        # GIVEN
        sut = TocGenerator()
        # WHEN
        actual_list = sut.generate(toc_node_list)
        # THEN
        for actual, expected in zip(actual_list, expected_list):
            assert actual == expected

    # 複数の根から目次を組み立てられるか
    @pytest.mark.parametrize(
        ('toc_node_list', 'expected_list'),
        [
            (
                [
                    TocNode(depth=1, text='概要その1', children=[]),
                    TocNode(depth=1, text='概要その2', children=[]),
                ],
                [
                    ListBlock(indent_depth=0, children=[
                        ListItemBlock(indent_depth=1, children=[
                            LinkInline(href='#概要その1', text='概要その1')
                        ])
                    ]),
                    ListBlock(indent_depth=0, children=[
                        ListItemBlock(indent_depth=1, children=[
                            LinkInline(href='#概要その2', text='概要その2')
                        ])
                    ]),
                ]
            ),
            (
                [
                    TocNode(depth=2, text='犬', children=[
                        TocNode(depth=3, text='秋田の犬', children=[]),
                        TocNode(depth=3, text='四国の犬', children=[
                            TocNode(depth=4, text='四国犬', children=[])
                        ])
                    ]),
                    TocNode(depth=1, text='犬について', children=[
                        TocNode(depth=2, text='犬とは', children=[
                            TocNode(depth=3, text='かわいい', children=[])
                        ]),
                        TocNode(depth=2, text='犬という字について', children=[])
                    ])
                ],
                [
                    ListBlock(indent_depth=0, children=[
                        ListItemBlock(indent_depth=1, children=[
                            LinkInline(href='#犬', text='犬')
                        ]),
                        ListItemBlock(indent_depth=1, children=[
                            ListBlock(indent_depth=2, children=[
                                ListItemBlock(indent_depth=3, children=[
                                    LinkInline(href='#秋田の犬', text='秋田の犬'),
                                ]),
                                ListItemBlock(indent_depth=3, children=[
                                    LinkInline(href='#四国の犬', text='四国の犬')
                                ]),
                                ListItemBlock(indent_depth=3, children=[
                                    ListBlock(indent_depth=4, children=[
                                        ListItemBlock(indent_depth=5, children=[
                                            LinkInline(href='#四国犬', text='四国犬')
                                        ])
                                    ])
                                ])
                            ])
                        ])
                    ]),
                    ListBlock(indent_depth=0, children=[
                        ListItemBlock(indent_depth=1, children=[
                            LinkInline(href='#犬について', text='犬について')
                        ]),
                        ListItemBlock(indent_depth=1, children=[
                            ListBlock(indent_depth=2, children=[
                                ListItemBlock(indent_depth=3, children=[
                                    LinkInline(href='#犬とは', text='犬とは')
                                ]),
                                ListItemBlock(indent_depth=3, children=[
                                    ListBlock(indent_depth=4, children=[
                                        ListItemBlock(indent_depth=5, children=[
                                            LinkInline(href='#かわいい', text='かわいい')
                                        ])
                                    ])
                                ]),
                                ListItemBlock(indent_depth=3, children=[
                                    LinkInline(href='#犬という字について', text='犬という字について')
                                ])
                            ])
                        ])
                    ])
                ]
            )
        ]
    )
    def test_multiple_node(self, toc_node_list: list[TocNode], expected_list: list[ListBlock]):
        # GIVEN
        sut = TocGenerator()
        # WHEN
        actual_list = sut.generate(toc_node_list)
        # THEN
        for actual, expected in zip(actual_list, expected_list):
            assert actual == expected


class TestTocConverter:
    """ マークダウンのパース結果から目次を表現するul/li Block要素を組み立てられるか検証 """

    # マークダウンのパース結果を目次へ変換できるか
    @pytest.mark.parametrize(
        ('parse_result', 'expected_list'),
        [
            (
                ParseResult(content=[
                    HeadingBlock(size=1, children=[
                        PlainInline(text='概要')
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
                [
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
                    ])
                ]
            ),
        ]
    )
    def test_convert(self, parse_result: ParseResult, expected_list: list[ListBlock]):
        # GIVEN
        sut = TocConverter()
        # WHEN
        actual_list = sut.convert(parse_result)
        # THEN
        for actual, expected in zip(actual_list, expected_list):
            assert actual == expected
