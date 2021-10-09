from app.converter import Converter
from app.markdown.parser import ParseResult

from tests.util_equality import equal_for_parse_result
from tests.util_factory import create_block, create_inline


class TestConverter:
    """ マークダウン・HTMLを中継するオブジェクトの生成を検証 """

    def test_convert_plain(self):
        # GIVEN
        sut = Converter()
        parse_result = ParseResult([create_block('', [create_inline('', 'Hello World')])])
        expected = parse_result

        # WHEN
        actual = sut.convert(parse_result)
        # THEN
        assert equal_for_parse_result(actual, expected)
