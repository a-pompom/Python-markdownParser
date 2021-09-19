from app.converter import Converter
from app.markdown_parser import ParseResult
from app.element.style import Plain
from app.element.block import PlainBlock

from tests.util import equal_for_parse_result


class TestConverter:

    def test_convert_plain(self):
        # GIVEN
        sut = Converter()
        expected = ParseResult([PlainBlock(Plain(), 'HelloWorld')])

        # WHEN
        actual = sut.convert(ParseResult([PlainBlock(Plain(), 'HelloWorld')]))
        # THEN
        assert equal_for_parse_result(actual, expected)
