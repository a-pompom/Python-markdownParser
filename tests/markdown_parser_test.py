import pytest

from app.markdown_parser import MarkdownParser, ParseResult, Block, HeadingParser
from app.element.block import PlainBlock
from app.element.style import Plain, Heading
from tests.util import equal_for_parse_result


class TestMarkdownParser:

    def test_plain(self):
        # GIVEN
        sut = MarkdownParser()
        expected = ParseResult([PlainBlock(Plain(), 'HelloWorld')])
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

        @pytest.mark.parametrize(('heading_text', 'heading_size', 'text'), [
            ('# this is heading', 1, 'this is heading'),
            ('###  3rd heading', 3, ' 3rd heading'),
        ], ids=['1st heading', '3rd heading'])
        def test_parse(self, heading_text: str, heading_size: int, text: str):
            # GIVEN
            sut = HeadingParser()
            # WHEN
            actual = sut.parse(heading_text)
            assert isinstance(actual.style, Heading) and actual.style.size == heading_size
            assert actual.children[0] == text
