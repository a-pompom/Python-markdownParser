import pytest

from app.markdown.parser import MarkdownParser, ParseResult
from tests.util_equality import equal_for_parse_result
from tests.util_factory import create_inline, create_block


class TestMarkdownParser:
    """ Block/Inlineをまとめて扱い、行文字列からマークダウンのパース結果を生成する機能を検証 """

    # パース結果
    @pytest.mark.parametrize(('lines', 'expected'), [
        (
                ['plain text'],
                ParseResult([create_block('', [create_inline('', 'plain text')])])
        ),
        (
                ['## awesome heading'],
                ParseResult([create_block('heading', [create_inline('', 'awesome heading')], size=2)])
        )
    ], ids=['plain', 'heading'])
    def test_parse(self, lines: list[str], expected: ParseResult):
        # GIVEN
        sut = MarkdownParser()
        # WHEN
        actual = sut.parse(lines)
        # THEN
        assert equal_for_parse_result(actual, expected)
