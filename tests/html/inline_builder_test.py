import pytest

from app.element.inline import Inline, LinkInline
from app.html.inline_builder import InlineBuilder, LinkBuilder

from tests.util_factory import create_inline


class TestInlineBuilder:
    """ Inline要素からHTML文字列が得られるか検証 """

    # HTML組み立て
    @pytest.mark.parametrize(('inline', 'expected'), [
        (create_inline('', 'plain text'), 'plain text'),
        (
            create_inline(
                'link',
                '参考リンク',
                href='https://docs.python.org/3/'
            ),
            '<a href="https://docs.python.org/3/">参考リンク</a>'
        ),
    ], ids=['plain', 'link'])
    def test_build(self, inline: Inline, expected: str):
        # GIVEN
        sut = InlineBuilder()
        # WHEN
        actual = sut.build(inline)
        # THEN
        assert actual == expected


class TestLinkBuilder:
    """ LinkInline要素からaタグと対応するHTML文字列が得られるか検証 """

    # 対象判定
    @pytest.mark.parametrize(('inline', 'expected'), [
        (create_inline('link', 'this is a link', href='url'), True),
        (create_inline('', 'plain text'), False),
        (create_inline('link', '参考リンク', href='https://www.google.com/'), True),
    ], ids=['target', 'not target', 'normal link'])
    def test_target(self, inline: Inline, expected: bool):
        # GIVEN
        sut = LinkBuilder()
        # WHEN
        actual = sut.is_target(inline)
        # THEN
        assert actual == expected

    # HTML組み立て
    @pytest.mark.parametrize(('inline', 'expected'), [
        (create_inline('link', 'this is a link', href='url'), '<a href="url">this is a link</a>'),
        (create_inline('link', '参考リンク', href='https://www.google.com/'), '<a href="https://www.google.com/">参考リンク</a>')
    ], ids=['url', 'google'])
    def test_build(self, inline: LinkInline, expected: str):
        # GIVEN
        sut = LinkBuilder()
        # WHEN
        actual = sut.build(inline)
        # THEN
        assert actual == expected
