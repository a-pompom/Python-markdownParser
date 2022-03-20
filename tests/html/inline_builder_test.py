import pytest

from a_pompom_markdown_parser.element.inline import Inline, PlainInline, LinkInline, CodeInline, ImageInline
from a_pompom_markdown_parser.html.inline_builder import InlineBuilder, LinkBuilder, CodeBuilder, ImageBuilder
from a_pompom_markdown_parser.settings import setting


class TestInlineBuilder:
    """ Inline要素からHTML文字列が得られるか検証 """

    # HTML組み立て
    @pytest.mark.parametrize(
        ('inline', 'expected'),
        [
            (
                PlainInline(text='plain text'),
                'plain text'
            ),
            (
                LinkInline(href='https://docs.python.org/3/', text='参考リンク'),
                (f'<a'
                 f' href="https://docs.python.org/3/"'
                 f' class="{setting["class_name"]["a"]}">'
                 f'参考リンク'
                 f'</a>')
            ),
            (
                ImageInline(src='image.png', alt='awesome image', text=''),
                '<img src="image.png" alt="awesome image">'
            ),
            (
                CodeInline(text='DependencyInjection'),
                (f'<code'
                 f' class="{setting["class_name"]["code"]}">'
                 f'DependencyInjection'
                 f'</code>')
            ),
        ],
        ids=['plain', 'link', 'image', 'code'])
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
    @pytest.mark.parametrize(
        ('inline', 'expected'),
        [
            (
                LinkInline(href='url', text='this is a link'),
                True
            ),
            (
                PlainInline(text='plain text'),
                False
            ),
            (
                LinkInline(href='https://www.google.com/', text='参考リンク'),
                True
            ),
        ],
        ids=['target', 'not target', 'normal link'])
    def test_target(self, inline: Inline, expected: bool):
        # GIVEN
        sut = LinkBuilder()
        # WHEN
        actual = sut.is_target(inline)
        # THEN
        assert actual == expected

    # HTML組み立て
    @pytest.mark.parametrize(
        ('inline', 'expected'),
        [
            (
                LinkInline(href='url', text='this is a link'),
                (f'<a href="url"'
                 f' class="{setting["class_name"]["a"]}">'
                 f'this is a link'
                 f'</a>')
            ),
            (
                LinkInline(href='https://www.google.com/', text='参考リンク'),
                (f'<a href="https://www.google.com/"'
                 f' class="{setting["class_name"]["a"]}">'
                 f'参考リンク'
                 f'</a>')
            )
        ],
        ids=['url', 'google'])
    def test_build(self, inline: LinkInline, expected: str):
        # GIVEN
        sut = LinkBuilder()

        # WHEN
        actual = sut.build(inline)
        # THEN
        assert actual == expected


class TestCodeBuilder:
    """ CodeInline要素からcodeタグと対応するHTML文字列が得られるか検証 """

    # 対象判定
    @pytest.mark.parametrize(
        ('inline', 'expected'), [
            (
                CodeInline(text='#'),
                True
            ),
            (
                LinkInline(href='url', text='this is a link'),
                False
            )
        ],
        ids=['target', 'not target'])
    def test_target(self, inline: Inline, expected: bool):
        # GIVEN
        sut = CodeBuilder()
        # WHEN
        actual = sut.is_target(inline)
        # THEN
        assert actual == expected

    # HTML組み立て
    @pytest.mark.parametrize(
        ('inline', 'expected'), [
            (
                CodeInline(text='plain text'),
                (f'<code'
                 f' class="{setting["class_name"]["code"]}">'
                 f'plain text'
                 f'</code>')
            ),
            (
                CodeInline(text='codeタグ'),
                (f'<code'
                 f' class="{setting["class_name"]["code"]}">'
                 f'codeタグ'
                 f'</code>')
            ),
        ],
        ids=['plain', 'full width'])
    def test_build(self, inline: CodeInline, expected: str):
        # GIVEN
        sut = CodeBuilder()
        # WHEN
        actual = sut.build(inline)
        # THEN
        assert actual == expected


class TestImageBuilder:
    """ ImageInline要素からimgタグと対応するHTML文字列が得られるか検証 """

    # 対象判定
    @pytest.mark.parametrize(
        ('inline', 'expected'),
        [
            (
                ImageInline(src='image.pn', alt='image', text=''),
                True
            ),
            (
                CodeInline(text='code text'),
                False
            )
        ],
        ids=['target', 'not target'])
    def test_target(self, inline: Inline, expected: bool):
        # GIVEN
        sut = ImageBuilder()
        # WHEN
        actual = sut.is_target(inline)
        # THEN
        assert actual == expected

    # HTML組み立て
    @pytest.mark.parametrize(
        ('inline', 'expected'),
        [
            (
                ImageInline(src='images/dog.png', alt='わんこ', text=''),
                '<img src="images/dog.png" alt="わんこ">'
            ),
            (
                ImageInline(src='http://localhost/image.png', alt='画像', text=''),
                '<img src="http://localhost/image.png" alt="画像">'
            ),
        ],
        ids=['path_expression', 'url_expression'])
    def test_build(self, inline: ImageInline, expected: str):
        # GIVEN
        sut = ImageBuilder()
        # WHEN
        actual = sut.build(inline)
        # THEN
        assert actual == expected
