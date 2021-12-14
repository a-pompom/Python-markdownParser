import pytest

from app.html.builder import HtmlBuilder
from app.element.block import ParseResult
from app.markdown.parser import MarkdownParser
from app.converter.converter import Converter


class TestHtmlBuilder:
    """ ParseResult要素からHTML文字列が組み立てられるか検証 """

    # HTML文字列の組み立て
    @pytest.mark.parametrize(
        ('parse_result', 'expected'),
        [
            (MarkdownParser().parse(['plain text']), 'plain text'),

            (MarkdownParser().parse(['#### 課題: 頑張りたい']), '<h4>課題: 頑張りたい</h4>'),

            (MarkdownParser().parse(['[参考](https://www.google.com/)']), '<a href="https://www.google.com/">参考</a>'),

            (MarkdownParser().parse(['### [Python](https://docs.python.org/3/)とは']),
             '<h3><a href="https://docs.python.org/3/">Python</a>とは</h3>'),
        ],
        ids=['plain', 'only block', 'only inline', 'block and inline'])
    def test_build(self, parse_result: ParseResult, expected: str):
        # GIVEN
        sut = HtmlBuilder()
        # WHEN
        actual = sut.build(parse_result)
        # THEN
        assert actual == expected

    # リストの組み立て
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (['* task 1', '* task 2', '* task 3'],
             '<ul><li>task 1</li><li>task 2</li><li>task 3</li></ul>')
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
             ('<pre><code>'
              '# コメントしておきます。'
              'const i = 0;'
              '</code></pre>')),

            (['```', 'someFunction()', '> コードは終わっているはず。'],
             ('<pre><code>'
              'someFunction()'
              '> コードは終わっているはず。'
              '</code></pre>')),
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
