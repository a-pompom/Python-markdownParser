import pytest

from app.element.inline import Inline
from app.html.inline_builder import InlineBuilder, LinkBuilder, CodeBuilder, ImageBuilder
from app.markdown.inline_parser import InlineParser, LinkParser, CodeParser, ImageParser


# TODO
# パラメータ部分をInline型として、`ImageParser().parse('text')`の結果を渡せるようにしたい

class TestInlineBuilder:
    """ Inline要素からHTML文字列が得られるか検証 """

    # HTML組み立て
    @pytest.mark.parametrize(
        ('inline_text', 'expected'),
        [
            ('plain text', 'plain text'),
            ('[参考リンク](https://docs.python.org/3/)', '<a href="https://docs.python.org/3/">参考リンク</a>'),
            ('![awesome image](image.png)', '<img src="image.png" alt="awesome image">'),
            ('`DependencyInjection`', '<code>DependencyInjection</code>'),
        ],
        ids=['plain', 'link', 'image', 'code'])
    def test_build(self, inline_text: str, expected: str):
        # GIVEN
        sut = InlineBuilder()
        # TODO: パラメータ部分にて、各パーサでパースした結果を渡せるようにしたい
        inline = InlineParser().parse(inline_text)[0]
        # WHEN
        actual = sut.build(inline)
        # THEN
        assert actual == expected


class TestLinkBuilder:
    """ LinkInline要素からaタグと対応するHTML文字列が得られるか検証 """

    # 対象判定
    @pytest.mark.parametrize(
        ('inline_text', 'expected'),
        [
            ('[this is a link](url)', True),
            ('plain text', False),
            ('[参考リンク](https://www.google.com/)', True)
        ],
        ids=['target', 'not target', 'normal link'])
    def test_target(self, inline_text: str, expected: bool):
        # GIVEN
        sut = LinkBuilder()
        inline = InlineParser().parse(inline_text)[0]
        # WHEN
        actual = sut.is_target(inline)
        # THEN
        assert actual == expected

    # HTML組み立て
    @pytest.mark.parametrize(
        ('inline_text', 'expected'),
        [
            ('[this is a link](url)', '<a href="url">this is a link</a>'),
            ('[参考リンク](https://www.google.com/)', '<a href="https://www.google.com/">参考リンク</a>')
        ],
        ids=['url', 'google'])
    def test_build(self, inline_text: str, expected: str):
        # GIVEN
        sut = LinkBuilder()
        inline = LinkParser().parse(inline_text)[1]

        # WHEN
        actual = sut.build(inline)
        # THEN
        assert actual == expected


class TestCodeBuilder:
    """ CodeInline要素からcodeタグと対応するHTML文字列が得られるか検証 """

    # 対象判定
    @pytest.mark.parametrize(
        ('inline_text', 'expected'), [
            ('`#`', True),
            ('[this is a link](url)', False),
        ],
        ids=['target', 'not target'])
    def test_target(self, inline_text: str, expected: bool):
        # GIVEN
        sut = CodeBuilder()
        inline = InlineParser().parse(inline_text)[0]
        # WHEN
        actual = sut.is_target(inline)
        # THEN
        assert actual == expected

    # HTML組み立て
    @pytest.mark.parametrize(
        ('inline_text', 'expected'), [
            ('`plain text`', '<code>plain text</code>'),
            ('`codeタグ`', '<code>codeタグ</code>'),
        ],
        ids=['plain', 'full width'])
    def test_build(self, inline_text: str, expected: str):
        # GIVEN
        sut = CodeBuilder()
        inline = CodeParser().parse(inline_text)[1]
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
            (ImageParser().parse('![image](image.png)')[1], True),
            (CodeParser().parse('`code text`')[1], False),
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
        ('inline_text', 'expected'),
        [
            ('![わんこ](images/dog.png)', '<img src="images/dog.png" alt="わんこ">'),
            ('![画像](http://localhost/image.png)', '<img src="http://localhost/image.png" alt="画像">'),
        ],
        ids=['path_expression', 'url_expression'])
    def test_build(self, inline_text, expected: str):
        # GIVEN
        sut = ImageBuilder()
        inline = ImageParser().parse(inline_text)[1]
        # WHEN
        actual = sut.build(inline)
        # THEN
        assert actual == expected
