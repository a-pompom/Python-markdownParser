from app.converter import Converter
from app.markdown_parser import Block, ParseResult

from tests.util import equal_for_parse_result


class TestConverter:

    def test_convert_plain(self):
        # GIVEN
        sut = Converter()
        expected = ParseResult([Block('', ['HelloWorld'])])

        # WHEN
        actual = sut.convert(ParseResult([Block('', ['HelloWorld'])]))
        # THEN
        assert equal_for_parse_result(actual, expected)
