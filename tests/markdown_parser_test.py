import pytest

from app.markdown_parser import MarkdownParser, ParseResult, Block, HeadingParser
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

    class TestHeading:

        @pytest.mark.parametrize(('text', 'expected'), [
            ('# this is heading', True),
            ('this is not heading', False),
            ('###Without space', False),
            ('＃FullWidth character', False)
        ], ids=['heading', 'not heading', 'no space', 'FullWidth'])
        def test_target(self, text: str, expected: bool):
            # GIVEN
            sut = HeadingParser()
            # WHEN
            actual = sut.is_target(text)
            # THEN
            assert actual == expected

        def test_parse(self):
            # GIVEN
            sut = HeadingParser()
            # WHEN
            actual = sut.parse('# This is Heading')
            assert actual.style == 'Heading'
            assert actual.children[0] == 'This is Heading'
