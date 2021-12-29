import pytest

from app.html.builder import HtmlBuilder
from app.element.block import ParseResult
from app.markdown.parser import MarkdownParser
from app.converter.converter import Converter

from app.settings import setting

LINE_BREAK = setting['newline_code']
INDENT = setting['indent']


class TestHtmlBuilder:
    """ ParseResult要素からHTML文字列が組み立てられるか検証 """

    # HTML文字列の組み立て
    @pytest.mark.parametrize(
        ('parse_result', 'expected'),
        [
            (
                    MarkdownParser().parse(['plain text']),
                    (
                            f'<p class="{setting["class_name"]["p"]}">{LINE_BREAK}'
                            f'{INDENT}plain text{LINE_BREAK}'
                            f'</p>{LINE_BREAK}'
                    )
            ),

            (
                    MarkdownParser().parse(['#### 課題: 頑張りたい']),
                    (
                            f'<h4 class="{setting["class_name"]["h4"]}">{LINE_BREAK}'
                            f'{INDENT}課題: 頑張りたい{LINE_BREAK}'
                            f'</h4>{LINE_BREAK}'
                    )
            ),

            (
                    MarkdownParser().parse(['[参考](https://www.google.com/)']),
                    (
                            f'<p class="{setting["class_name"]["p"]}">{LINE_BREAK}'
                            f'{INDENT}<a href="https://www.google.com/" class="{setting["class_name"]["a"]}">参考</a>{LINE_BREAK}'
                            f'</p>{LINE_BREAK}'
                    )
            ),

            (
                    MarkdownParser().parse(['### [Python](https://docs.python.org/3/)とは']),
                    (
                            f'<h3 class="{setting["class_name"]["h3"]}">{LINE_BREAK}'
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
        ('lines', 'expected'),
        [
            (
                    ['> 私は昨日こう言いました', '> 帰りたいなぁ', '> 引用終わり'],
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
    def test_build_quote(self, lines: list[str], expected: str):
        sut = HtmlBuilder()
        parse_result = Converter().convert(MarkdownParser().parse(lines))
        # WHEN
        actual = sut.build(parse_result)
        # THEN
        assert actual == expected

    # リストの組み立て
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (
                    ['* task 1', '* task 2', '* task 3'],
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
            )
        ]
    )
    def test_build_list(self, lines: list[str], expected: str):
        sut = HtmlBuilder()
        parse_result = Converter().convert(MarkdownParser().parse(lines))
        # WHEN
        actual = sut.build(parse_result)
        # THEN
        assert actual == expected

    # コードブロックの組み立て
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (['```', '# コメントしておきます。', 'const i = 0;', '```'],
             (f'<pre>{LINE_BREAK}'
              f'{INDENT}<code>{LINE_BREAK}'
              f'{INDENT}{INDENT}# コメントしておきます。{LINE_BREAK}'
              f'{INDENT}{INDENT}const i = 0;{LINE_BREAK}'
              f'{INDENT}</code>{LINE_BREAK}'
              f'</pre>{LINE_BREAK}')),

            (['```', 'someFunction()', '> コードは終わっているはず。'],
             (f'<pre>{LINE_BREAK}'
              f'{INDENT}<code>{LINE_BREAK}'
              f'{INDENT}{INDENT}someFunction(){LINE_BREAK}'
              f'{INDENT}{INDENT}> コードは終わっているはず。{LINE_BREAK}'
              f'{INDENT}</code>{LINE_BREAK}'
              f'</pre>{LINE_BREAK}'))

            ,
        ],
        ids=['has end', 'no end']
    )
    def test_build_code_list(self, lines: list[str], expected: str):
        sut = HtmlBuilder()
        parse_result = Converter().convert(MarkdownParser().parse(lines))
        # WHEN
        actual = sut.build(parse_result)
        # THEN
        assert actual == expected
