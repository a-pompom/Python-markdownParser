from app.html_builder import HtmlBuilder
from app.markdown_parser import ParseResult, Inline, Block


class TestHtmlBuilder:

    # とりあえずプレーンテキストを処理
    def test_build(self):

        # GIVEN
        expected = 'Hello World'
        input = ParseResult([Block('', ['Hello World'])])
        sut = HtmlBuilder()

        # WHEN
        actual = sut.build(input)
        # THEN
        assert actual == expected
