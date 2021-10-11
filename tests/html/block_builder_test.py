import pytest

from app.html.block_builder import BlockBuilder, HeadingBuilder
from app.element.block import Block, HeadingBlock

from tests.util_factory import create_block, create_inline


class TestBlockBuilder:
    """ Block要素からHTML文字列が得られるか検証 """

    # HTML文字列組み立て
    @pytest.mark.parametrize(('block', 'child_text', 'expected'), [
        (
            create_block('', [create_inline('', 'plain text')]),
            'plain text',
            'plain text'
        ),
        (
            create_block('heading', [create_inline('', '概要')], size=1),
            '概要',
            '<h1>概要</h1>'
        ),
    ], ids=['plain', 'heading'])
    def test_build(self, block: Block, child_text: str, expected: str):
        # GIVEN
        sut = BlockBuilder()
        # WHEN
        actual = sut.build(block, child_text)
        # THEN
        assert actual == expected


class TestHeadingBuilder:
    """ HeadingBlock要素からヘッダと対応するHTML文字列を組み立てられるか検証 """

    # 対象判定
    @pytest.mark.parametrize(('block', 'expected'), [
        (create_block('heading', [create_inline('', '# this is a heading')], size=1), True),
        (create_block('', [create_inline('', 'plain text')]), False),
    ], ids=['target', 'not target'])
    def test_target(self, block: Block, expected: bool):
        # GIVEN
        sut = HeadingBuilder()
        # WHEN
        actual = sut.is_target(block)
        # THEN
        assert actual == expected

    # HTML文字列組み立て
    @pytest.mark.parametrize(('block', 'child_text', 'expected'), [
        (
            create_block('heading', [create_inline('', 'first heading')], size=1),
            'first heading',
            '<h1>first heading</h1>'
        ),
        (
            create_block('heading', [create_inline('', '補足: これは補足です')], size=4),
            '補足: これは補足です',
            '<h4>補足: これは補足です</h4>'
        ),
    ], ids=['first', '4th'])
    def test_build(self, block: HeadingBlock, child_text: str, expected: str):
        # THEN
        sut = HeadingBuilder()
        # WHEN
        actual = sut.build(block, child_text)
        # THEN
        assert actual == expected
