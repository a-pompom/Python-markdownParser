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

            (Converter().convert(MarkdownParser().parse(
                ['* task 1', '* task 2', '* task 3']
            )), '<ul><li>task 1</li><li>task 2</li><li>task 3</li></ul>')
        ],
        ids=['plain', 'only block', 'only inline', 'block and inline', 'contain list'])
    def test_build(self, parse_result: ParseResult, expected: str):
        # GIVEN
        sut = HtmlBuilder()
        # WHEN
        actual = sut.build(parse_result)
        # THEN
        assert actual == expected
