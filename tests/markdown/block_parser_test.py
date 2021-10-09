import pytest

from app.markdown.block_parser import BlockParser, HeadingParser
from app.element.block import Block, Children
from app.element.style import Heading

from tests.util_equality import equal_for_block
from tests.util_factory import create_block, create_inline


class TestBlockParser:
    """ 行文字列・Inline要素からInline要素を子に持つBlock要素が生成されるか検証 """

    # 行の分解
    @pytest.mark.parametrize(('text', 'expected'), [
        ('plain text', 'plain text'),
        ('### awesome heading', 'awesome heading'),
    ], ids=['plain', 'heading'])
    def test_extract_inline_text(self, text: str, expected: str):
        # GIVEN
        sut = BlockParser()
        # WHEN
        actual = sut.extract_inline_text(text)
        # THEN
        assert actual == expected

    # Block要素生成
    @pytest.mark.parametrize(('text', 'children', 'expected'), [
        (
            'plain text',
            [create_inline('', 'plain text')],
            create_block('', [create_inline('', 'plain text')])
        ),
        (
            '## awesome heading',
            [create_inline('', 'awesome heading')],
            create_block('heading', [create_inline('', 'awesome heading')], size=2)
        )
    ], ids=['plain', 'heading'])
    def test_parse(self, text: str, children: Children, expected: Block):
        # GIVEN
        sut = BlockParser()
        # WHEN
        actual = sut.parse(text, children)
        # THEN
        assert equal_for_block(actual, expected)


class TestHeading:
    """ #で表現されるヘッダ要素 """

    # 記法が対象か
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

    # 記法の解釈
    @pytest.mark.parametrize(('heading_text', 'heading_size', 'children'), [
        (
                '# this is heading',
                1,
                [create_inline('', 'this is heading')]
        ),
        (
                '###  3rd heading',
                3,
                [create_inline('', ' 3rd heading')]
        ),
        (
                '## 2nd heading [link](url) text',
                2,
                [create_inline('', '2nd heading '), create_inline('link', 'link', href='url'),
                 create_inline('', ' text')]
        )
    ], ids=['1st heading', '3rd heading', '2nd heading with link'])
    def test_parse(self, heading_text: str, heading_size: int, children: Children):
        # GIVEN
        sut = HeadingParser()
        # WHEN
        actual = sut.parse(heading_text, children)

        # THEN
        assert isinstance(actual.style, Heading)
        assert equal_for_block(actual, create_block('heading', children, size=heading_size))
