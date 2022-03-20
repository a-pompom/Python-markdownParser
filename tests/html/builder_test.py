import pytest

from a_pompom_markdown_parser.html.builder import HtmlBuilder
from a_pompom_markdown_parser.element.block import ParseResult, HeadingBlock, ParagraphBlock, QuoteBlock, ListBlock, \
    ListItemBlock, CodeBlock, PlainBlock
from a_pompom_markdown_parser.element.inline import PlainInline, LinkInline

from a_pompom_markdown_parser.settings import setting

LINE_BREAK = setting['newline_code']
INDENT = setting['indent']


class TestHtmlBuilder:
    """ ParseResult要素からHTML文字列が組み立てられるか検証 """

    # HTML文字列の組み立て
    @pytest.mark.parametrize(
        ('parse_result', 'expected'),
        [
            (
                ParseResult(content=[
                    ParagraphBlock(indent_depth=0, children=[
                        PlainInline(text='plain text')
                    ])
                ]),
                (
                    f'<p class="{setting["class_name"]["p"]}">{LINE_BREAK}'
                    f'{INDENT}plain text{LINE_BREAK}'
                    f'</p>{LINE_BREAK}'
                )
            ),

            (
                ParseResult(content=[
                    HeadingBlock(size=4, children=[
                        PlainInline(text='課題: 頑張りたい')
                    ])
                ]),
                (
                    f'<h4 id="課題: 頑張りたい" class="{setting["class_name"]["h4"]}">{LINE_BREAK}'
                    f'{INDENT}課題: 頑張りたい{LINE_BREAK}'
                    f'</h4>{LINE_BREAK}'
                )
            ),

            (
                ParseResult(content=[
                    ParagraphBlock(indent_depth=0, children=[
                        LinkInline(href='https://www.google.com/', text='参考')
                    ])
                ]),
                (
                    f'<p class="{setting["class_name"]["p"]}">{LINE_BREAK}'
                    f'{INDENT}<a href="https://www.google.com/" class="{setting["class_name"]["a"]}">参考</a>{LINE_BREAK}'
                    f'</p>{LINE_BREAK}'
                )
            ),

            (
                ParseResult(content=[
                    HeadingBlock(size=3, children=[
                        LinkInline(href='https://docs.python.org/3/', text='Python'),
                        PlainInline(text='とは')
                    ])
                ]),
                (
                    f'<h3 id="Pythonとは" class="{setting["class_name"]["h3"]}">{LINE_BREAK}'
                    f'{INDENT}<a href="https://docs.python.org/3/" class="{setting["class_name"]["a"]}">Python</a>とは{LINE_BREAK}'
                    f'</h3>{LINE_BREAK}'
                )
            ),
        ],
        ids=['plain', 'only block', 'only inline', 'block and inline'])
    def test_build(self, parse_result: ParseResult, expected: str):
        # GIVEN
        sut = HtmlBuilder()
        # WHEN
        actual = sut.build(parse_result)
        # THEN
        assert actual == expected

    # 引用要素の組み立て
    @pytest.mark.parametrize(
        ('parse_result', 'expected'),
        [
            (
                ParseResult(content=[
                    QuoteBlock(children=[
                        ParagraphBlock(indent_depth=1, children=[
                            PlainInline(text='私は昨日こう言いました')
                        ]),
                        ParagraphBlock(indent_depth=1, children=[
                            PlainInline(text='帰りたいなぁ')
                        ]),
                        ParagraphBlock(indent_depth=1, children=[
                            PlainInline(text='引用終わり')
                        ]),
                    ])
                ]),
                (
                    f'<blockquote class="{setting["class_name"]["blockquote"]}">{LINE_BREAK}'
                    f'{INDENT}<p class="{setting["class_name"]["p"]}">{LINE_BREAK}'
                    f'{INDENT}{INDENT}私は昨日こう言いました{LINE_BREAK}'
                    f'{INDENT}</p>{LINE_BREAK}'

                    f'{INDENT}<p class="{setting["class_name"]["p"]}">{LINE_BREAK}'
                    f'{INDENT}{INDENT}帰りたいなぁ{LINE_BREAK}'
                    f'{INDENT}</p>{LINE_BREAK}'

                    f'{INDENT}<p class="{setting["class_name"]["p"]}">{LINE_BREAK}'
                    f'{INDENT}{INDENT}引用終わり{LINE_BREAK}'
                    f'{INDENT}</p>{LINE_BREAK}'

                    f'</blockquote>{LINE_BREAK}'
                )
            )
        ]
    )
    def test_build_quote(self, parse_result: ParseResult, expected: str):
        sut = HtmlBuilder()
        # WHEN
        actual = sut.build(parse_result)
        # THEN
        assert actual == expected

    # リストの組み立て
    @pytest.mark.parametrize(
        ('parse_result', 'expected'),
        [
            (
                ParseResult(content=[
                    ListBlock(indent_depth=0, children=[
                        ListItemBlock(indent_depth=1, children=[
                            PlainInline(text='task 1')
                        ]),
                        ListItemBlock(indent_depth=1, children=[
                            PlainInline(text='task 2')
                        ]),
                        ListItemBlock(indent_depth=1, children=[
                            PlainInline(text='task 3')
                        ]),
                    ])
                ]),
                (
                    f'<ul class="{setting["class_name"]["ul"]}">{LINE_BREAK}'
                    f'{INDENT}<li class="{setting["class_name"]["li"]}">{LINE_BREAK}'
                    f'{INDENT}{INDENT}task 1{LINE_BREAK}'
                    f'{INDENT}</li>{LINE_BREAK}'
                    f'{INDENT}<li class="{setting["class_name"]["li"]}">{LINE_BREAK}'
                    f'{INDENT}{INDENT}task 2{LINE_BREAK}'
                    f'{INDENT}</li>{LINE_BREAK}'
                    f'{INDENT}<li class="{setting["class_name"]["li"]}">{LINE_BREAK}'
                    f'{INDENT}{INDENT}task 3{LINE_BREAK}'
                    f'{INDENT}</li>{LINE_BREAK}'
                    f'</ul>{LINE_BREAK}'
                )
            ),
            (
                ParseResult(content=[
                    ListBlock(indent_depth=0, children=[
                        ListItemBlock(indent_depth=1, children=[
                            LinkInline(href='#概要', text='概要')
                        ]),
                        ListItemBlock(indent_depth=1, children=[
                            ListBlock(indent_depth=2, children=[
                                ListItemBlock(indent_depth=3, children=[
                                    LinkInline(href='#ゴール', text='ゴール')
                                ])
                            ])
                        ])
                    ]),
                ]),
                (
                    f'<ul class="{setting["class_name"]["ul"]}">{LINE_BREAK}'
                    f'{INDENT}<li class="{setting["class_name"]["li"]}">{LINE_BREAK}'
                    f'{INDENT}{INDENT}<a href="#概要" class="{setting["class_name"]["a"]}">概要</a>{LINE_BREAK}'
                    f'{INDENT}</li>{LINE_BREAK}'
                    f'{INDENT}<li class="{setting["class_name"]["li_nested"]}">{LINE_BREAK}'
                    f'{INDENT}{INDENT}<ul class="{setting["class_name"]["ul"]}">{LINE_BREAK}'
                    f'{INDENT}{INDENT}{INDENT}<li class="{setting["class_name"]["li"]}">{LINE_BREAK}'
                    f'{INDENT}{INDENT}{INDENT}{INDENT}<a href="#ゴール" class="{setting["class_name"]["a"]}">ゴール</a>{LINE_BREAK}'
                    f'{INDENT}{INDENT}{INDENT}</li>{LINE_BREAK}'
                    f'{INDENT}{INDENT}</ul>{LINE_BREAK}'
                    f'{INDENT}</li>{LINE_BREAK}'
                    f'</ul>{LINE_BREAK}'
                )
            )
        ],
        ids=['single', 'nested']
    )
    def test_build_list(self, parse_result: ParseResult, expected: str):
        sut = HtmlBuilder()
        # WHEN
        actual = sut.build(parse_result)
        # THEN
        assert actual == expected

    # コードブロックの組み立て
    @pytest.mark.parametrize(
        ('parse_result', 'expected'),
        [
            (
                ParseResult(content=[
                    CodeBlock(language='', children=[
                        PlainBlock(indent_depth=0, children=[
                            PlainInline(text='# コメントしておきます。')
                        ]),
                        PlainBlock(indent_depth=0, children=[
                            PlainInline(text='const i = 0;')
                        ]),
                    ])
                ]),
                (f'<pre>{LINE_BREAK}'
                 f'{INDENT}<code class="language- hljs">{LINE_BREAK}'
                 f'# コメントしておきます。{LINE_BREAK}'
                 f'const i = 0;{LINE_BREAK}'
                 f'{INDENT}</code>{LINE_BREAK}'
                 f'</pre>{LINE_BREAK}')
            ),

            (
                ParseResult(content=[
                    CodeBlock(language='JavaScript', children=[
                        PlainBlock(indent_depth=0, children=[
                            PlainInline(text='someFunction()')
                        ]),
                        PlainBlock(indent_depth=0, children=[
                            PlainInline(text='> コードは終わっているはず。')
                        ]),
                    ])
                ]),
                (f'<pre>{LINE_BREAK}'
                 f'{INDENT}<code class="language-javascript hljs">{LINE_BREAK}'
                 f'someFunction(){LINE_BREAK}'
                 f'> コードは終わっているはず。{LINE_BREAK}'
                 f'{INDENT}</code>{LINE_BREAK}'
                 f'</pre>{LINE_BREAK}')
            ),
        ],
        ids=['has end', 'no end']
    )
    def test_build_code_list(self, parse_result: ParseResult, expected: str):
        sut = HtmlBuilder()
        # WHEN
        actual = sut.build(parse_result)
        # THEN
        assert actual == expected
