import pytest

from app.html_builder import HtmlBuilder, HeadingBuilder
from app.markdown_parser import ParseResult
from app.element.style import Plain, Heading
from app.element.inline import PlainInline
from app.element.block import PlainBlock, HeadingBlock


class TestHtmlBuilder:

    # とりあえずプレーンテキストを処理
    def test_build(self):

        # GIVEN
        expected = 'Hello World'
        html_input = ParseResult([PlainBlock(Plain(), [PlainInline(Plain(), 'Hello World')])])
        sut = HtmlBuilder()

        # WHEN
        actual = sut.build(html_input)
        # THEN
        assert actual == expected

    class TestHeading:

        @pytest.mark.parametrize(('block', 'expected'), [
            (HeadingBlock(Heading(size=1), [PlainInline(Plain(), 'this is 1st heading')]), '<h1>this is 1st heading</h1>'),
            (HeadingBlock(Heading(size=4), [PlainInline(Plain(), 'this is 4th heading')]), '<h4>this is 4th heading</h4>'),

        ], ids=['1st heading', '4th heading'])
        def test_build(self, block: HeadingBlock, expected: str):

            # GIVEN
            sut = HeadingBuilder()
            # WHEN
            actual = sut.build(block)
            # THEN
            assert actual == expected
