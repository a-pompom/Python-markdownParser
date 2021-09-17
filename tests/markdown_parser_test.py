from app.markdown_parser import MarkdownParser, ParseResult, Block
from tests.util import equal_for_parse_result


class TestMarkdownParser:

    def test_plain(self):
        # GIVEN
        sut = MarkdownParser()
        expected = ParseResult([Block('', ['HelloWorld'])])
        # WHEN
        actual = sut.parse(['HelloWorld'])
        # THEN
        assert equal_for_parse_result(actual, expected)
