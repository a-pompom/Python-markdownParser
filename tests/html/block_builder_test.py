import pytest

from app.html.block_builder import BlockBuilder, HeadingBuilder, QuoteBuilder
from app.markdown.block_parser import BlockParser, HeadingParser, QuoteParser
from app.markdown.inline_parser import InlineParser


class TestBlockBuilder:
    """ Block要素からHTML文字列が得られるか検証 """

    # HTML文字列組み立て
    @pytest.mark.parametrize(
        ('block_text', 'child_text', 'expected'),
        [
            ('plain text', 'plain text', 'plain text'),
            ('# 概要', '概要', '<h1>概要</h1>'),
            ('> と言いました', 'と言いました', '<blockquote>と言いました</blockquote>')
        ],
        ids=['plain', 'heading', 'quote'])
    def test_build(self, block_text: str, child_text: str, expected: str):
        # GIVEN
        sut = BlockBuilder()
        block = BlockParser().parse(block_text, InlineParser().parse(child_text))
        # WHEN
        actual = sut.build(block, child_text)
        # THEN
        assert actual == expected


class TestHeadingBuilder:
    """ HeadingBlock要素からヘッダと対応するHTML文字列を組み立てられるか検証 """

    # 対象判定
    @pytest.mark.parametrize(
        ('block_text', 'child_text', 'expected'),
        [
            ('# this is a heading', 'this is a heading', True),
            ('plain text', 'plain text', False),
        ],
        ids=['target', 'not target'])
    def test_target(self, block_text: str, child_text: str, expected: bool):
        # GIVEN
        sut = HeadingBuilder()
        block = BlockParser().parse(block_text, InlineParser().parse(child_text))
        # WHEN
        actual = sut.is_target(block)
        # THEN
        assert actual == expected

    # HTML文字列組み立て
    @pytest.mark.parametrize(
        ('block_text', 'child_text', 'expected'),
        [
            ('# first heading', 'first heading', '<h1>first heading</h1>'),
            ('#### 補足: これは補足です', '補足: これは補足です', '<h4>補足: これは補足です</h4>')
        ],
        ids=['first', '4th'])
    def test_build(self, block_text: str, child_text: str, expected: str):
        # THEN
        sut = HeadingBuilder()
        block = HeadingParser().parse(block_text, InlineParser().parse(child_text))
        # WHEN
        actual = sut.build(block, child_text)
        # THEN
        assert actual == expected


class TestQuoteBuilder:
    """ blockquoteタグ文字列の組み立てを検証 """

    @pytest.mark.parametrize(
        ('block_text', 'child_text', 'expected'),
        [
            ('> これは引用です', 'これは引用です', True),
            ('[参考](url)', '[参考](url)', False)
        ],
        ids=['target', 'not target']
    )
    def test_is_target(self, block_text: str, child_text: str, expected: bool):
        # GIVEN
        sut = QuoteBuilder()
        block = BlockParser().parse(block_text, InlineParser().parse(child_text))
        # WHEN
        actual = sut.is_target(block)
        # THEN
        assert actual == expected

    @pytest.mark.parametrize(
        ('block_text', 'child_text', 'expected'),
        [
            ('> それが問題です', 'それが問題です', '<blockquote>それが問題です</blockquote>')
        ],
        ids=['quote']
    )
    def test_build(self, block_text: str, child_text: str, expected: str):
        # GIVEN
        sut = QuoteBuilder()
        block = QuoteParser().parse(block_text, InlineParser().parse(child_text))
        # WHEN
        actual = sut.build(block, child_text)
        # THEN
        assert actual == expected
