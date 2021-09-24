import pytest

from app.markdown.parser import MarkdownParser, ParseResult, HeadingParser, LinkParser
from app.element.block import PlainBlock, HeadingBlock, Children
from app.element.inline import PlainInline, LinkInline
from app.element.style import Plain, Heading, Link
from tests.util import equal_for_parse_result, equal_for_inline_parse_result, equal_for_block


def test_plain(self):
    # GIVEN
    sut = MarkdownParser()
    expected = ParseResult([PlainBlock(Plain(), [PlainInline(Plain(), 'Hello World')])])
    # WHEN
    actual = sut.parse(['Hello World'])
    # THEN
    assert equal_for_parse_result(actual, expected)


class TestInline:

    class TestLink:

        @pytest.mark.parametrize(('text', 'expected'), [
            ('this is [link](url)', True),
            ('this is not link', False),
            ('[only link](http://www)', True)
        ], ids=['link text', 'not link', 'only link'])
        def test_target(self, text: str, expected: bool):
            sut = LinkParser()
            # WHEN
            actual = sut.is_target(text)
            # THEN
            assert actual == expected

        @pytest.mark.parametrize(('link_text', 'expected'), [
            ('normal[link](url)text', ('normal', LinkInline(Link('url'), 'link'), 'text')),
            ('[link](http)', ('', LinkInline(Link('http'), 'link'), '')),
            ('# heading [head link](https) text', ('# heading ', LinkInline(Link('https'), 'head link'), ' text')),
        ], ids=['normal link', 'only link', 'link with heading'])
        def test_parse(self, link_text: str, expected: tuple[str, LinkInline, str]):
            sut = LinkParser()
            # WHEN
            actual = sut.parse(link_text)
            # THEN
            assert equal_for_inline_parse_result(actual, expected)


class TestBlock:

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

        @pytest.mark.parametrize(('heading_text', 'heading_size', 'children'), [
            (
                '# this is heading',
                1,
                [PlainInline(Plain(), 'this is heading')]
            ),
            (
                '###  3rd heading',
                3,
                [PlainInline(Plain(), ' 3rd heading')]
            ),
            (
                '## 2nd heading [link](url) text',
                2,
                [PlainInline(Plain(), '2nd heading '), LinkInline(Link('url'), 'link'), PlainInline(Plain(), ' text')]
            )
        ], ids=['1st heading', '3rd heading', '2nd heading with link'])
        def test_parse(self, heading_text: str, heading_size: int, children: Children):
            # GIVEN
            sut = HeadingParser()
            # WHEN
            actual = sut.parse(heading_text, children)

            # THEN
            assert isinstance(actual.style, Heading)
            assert equal_for_block(actual, HeadingBlock(Heading(heading_size), children))
