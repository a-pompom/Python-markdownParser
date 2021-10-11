import pytest

from app.html.builder import HtmlBuilder
from app.element.block import ParseResult

from tests.util_factory import create_block, create_inline


class TestHtmlBuilder:
    """ ParseResult要素からHTML文字列が組み立てられるか検証 """

    # HTML文字列の組み立て
    @pytest.mark.parametrize(('parse_result', 'expected'), [
        (
            ParseResult(content=[
                create_block('', [create_inline('', 'plain text')])
            ]),
            'plain text'
        ),
        (
            ParseResult(content=[
                create_block('heading', [create_inline('', '課題: 頑張りたい')], size=4)
            ]),
            '<h4>課題: 頑張りたい</h4>'
        ),
        (
            ParseResult(content=[
                create_block('', [create_inline('link', '参考:', href='https://www.google.com/')])
            ]),
            '<a href="https://www.google.com/">参考:</a>'
        ),
        (
            ParseResult(content=[
                create_block('heading', [
                    create_inline('link', 'Python', href='https://docs.python.org/3/'),
                    create_inline('', 'とは'),
                ], size=3)
            ]),
            '<h3><a href="https://docs.python.org/3/">Python</a>とは</h3>'
        ),
    ], ids=['plain', 'only block', 'only inline', 'block and inline'])
    def test_build(self, parse_result: ParseResult, expected: str):
        # GIVEN
        sut = HtmlBuilder()
        # WHEN
        actual = sut.build(parse_result)
        # THEN
        assert actual == expected
