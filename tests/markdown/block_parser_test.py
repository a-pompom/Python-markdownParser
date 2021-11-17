import pytest

from app.markdown.inline_parser import InlineParser
from app.markdown.block_parser import BlockParser, HeadingParser


class TestBlockParser:
    """ 行文字列・Inline要素からInline要素を子に持つBlock要素が生成されるか検証 """

    # 行の分解
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            ('plain text', 'plain text'),
            ('### awesome heading', 'awesome heading'),
        ],
        ids=['plain', 'heading'])
    def test_extract_inline_text(self, text: str, expected: str):
        # GIVEN
        sut = BlockParser()
        # WHEN
        actual = sut.extract_inline_text(text)
        # THEN
        assert actual == expected

    # Block要素生成
    @pytest.mark.parametrize(
        ('text', 'child_text', 'expected'),
        [
            (
                    'plain text',
                    'plain text',
                    '[Plain: | Child of Plain -> Plain: text=plain text]'
            ),
            (
                    '## awesome heading',
                    'awesome heading',
                    '[Heading: size=2 | Child of Heading -> Plain: text=awesome heading]'
            )
        ],
        ids=['plain', 'heading'])
    def test_parse(self, text: str, child_text: str, expected: str):
        # GIVEN
        sut = BlockParser()
        inline_parser = InlineParser()
        # WHEN
        children = inline_parser.parse(child_text)
        actual = sut.parse(text, children)

        # THEN
        assert repr(actual) == expected


class TestHeading:
    """ #で表現されるヘッダ要素 """

    # 記法が対象か
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            ('# this is heading', True),
            ('this is not heading', False),
            ('###Without space', False),
            ('＃FullWidth character', False)
        ],
        ids=['heading', 'not heading', 'no space', 'FullWidth'])
    def test_target(self, text: str, expected: bool):
        # GIVEN
        sut = HeadingParser()
        # WHEN
        actual = sut.is_target(text)
        # THEN
        assert actual == expected

    # 記法の解釈
    @pytest.mark.parametrize(
        ('heading_text', 'child_text', 'expected'),
        [
            (
                    '# this is heading',
                    'this is heading',
                    '[Heading: size=1 | Child of Heading -> Plain: text=this is heading]'
            ),
            (
                    '###  3rd heading',
                    ' 3rd heading',
                    '[Heading: size=3 | Child of Heading -> Plain: text= 3rd heading]'
            ),
            (
                    '## 2nd heading [link](url) text',
                    '2nd heading [link](url) text',
                    ('[Heading: size=2 | '
                     'Child of Heading -> Plain: text=2nd heading  | '
                     'Child of Heading -> Link: text=link, href=url | '
                     'Child of Heading -> Plain: text= text]')
            )
        ], ids=['1st heading', '3rd heading', '2nd heading with link'])
    def test_parse(self, heading_text: str, child_text: str, expected: str):
        # GIVEN
        sut = HeadingParser()
        inline_parser = InlineParser()
        # WHEN
        children = inline_parser.parse(child_text)
        actual = sut.parse(heading_text, children)

        # THEN
        assert repr(actual) == expected
