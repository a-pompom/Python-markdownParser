import pytest

from app.markdown.inline_parser import InlineParser, LinkParser, CodeParser, ImageParser
from app.element.inline import Inline, LinkInline, CodeInline, ImageInline
from app.element.style import Link
from tests.util_equality import equal_for_inline_parse_result, equal_for_inline
from tests.util_factory import create_inline


class TestInlineParser:
    """ 行文字列からインライン記法を表現するInline要素を生成できるか検証 """

    # Inline要素生成
    @pytest.mark.parametrize(('text', 'expected'), [
        (
                'plain text',
                [create_inline('', 'plain text')]
        ),
        (
                'this is [google link](https://www.google.com/)',
                [create_inline('', 'this is '), create_inline('link', 'google link', href='https://www.google.com/')]
        )
    ], ids=['plain', 'link'])
    def test_parse(self, text: str, expected: list[Inline]):
        sut = InlineParser()
        actual = sut.parse(text)

        for former, latter in zip(actual, expected):
            assert equal_for_inline(former, latter)


class TestLink:
    """ []()で表現されるリンク要素を検証 """

    # 記法が対象か
    @pytest.mark.parametrize(('text', 'expected'), [
        ('this is [link](url)', True),
        ('this is not link', False),
        ('[only link](http://www)', True),
        ('![image](http://www)', False)
    ], ids=['link text', 'not link', 'only link', 'image'])
    def test_target(self, text: str, expected: bool):
        sut = LinkParser()
        # WHEN
        actual = sut.is_target(text)
        # THEN
        assert actual == expected

    # 記法を解釈
    @pytest.mark.parametrize(('link_text', 'expected'), [
        ('normal[link](url)text', ('normal', LinkInline(Link('url'), 'link'), 'text')),
        ('[link](http)', ('', create_inline('link', 'link', href='http'), '')),
        (
                '# heading [head link](https) text',
                ('# heading ', create_inline('link', 'head link', href='https'), ' text')
        ),
        ('not ! image [link](url)text', ('not ! image ', LinkInline(Link('url'), 'link'), 'text')),
    ], ids=['normal link', 'only link', 'link with heading', 'not image'])
    def test_parse(self, link_text: str, expected: tuple[str, LinkInline, str]):
        sut = LinkParser()
        # WHEN
        actual = sut.parse(link_text)
        # THEN
        assert equal_for_inline_parse_result(actual, expected)


class TestCode:
    """ ``で表現されるコード要素を検証 """

    # 記法が対象か
    @pytest.mark.parametrize(('text', 'expected'), [
        ('Pythonのコメントは`#`で表現されます。', True),
        ('私はPythonが好きです', False),
    ], ids=['code', 'not code'])
    def test_target(self, text: str, expected: bool):
        # GIVEN
        sut = CodeParser()
        # WHEN
        actual = sut.is_target(text)
        # THEN
        assert actual == expected

    # 記法を解釈
    @pytest.mark.parametrize(('text', 'expected'), [
        ('`//`でコメントを表現します。', ['', create_inline('code', '//'), 'でコメントを表現します。']),
        ('JavaScriptの変数は`const`で宣言します。', ['JavaScriptの変数は', create_inline('code', 'const'), 'で宣言します。']),
        ('codeで終わります`。`', ['codeで終わります', create_inline('code', '。'), '']),
    ], ids=['no head', 'both', 'no tail'])
    def test_parse(self, text: str, expected: tuple[str, CodeInline, str]):
        # GIVEN
        sut = CodeParser()
        # WHEN
        actual = sut.parse(text)
        # THEN
        assert equal_for_inline_parse_result(actual, expected)


class TestImage:
    """ ![]()で表現される画像要素を検証 """

    # 対象判定
    @pytest.mark.parametrize(('text', 'expected'), [
        ('![画像](img.png)', True),
        ('[これはリンクです](https://www.google.com', False)
    ], ids=['target', 'not target'])
    def test_target(self, text: str, expected: bool):
        # GIVEN
        sut = ImageParser()
        # WHEN
        actual = sut.is_target(text)
        # THEN
        assert actual == expected

    # 記法を解釈
    @pytest.mark.parametrize(('text', 'expected'), [
        (
                '![awesome image](/image.png) is here.',
                (
                        '',
                        create_inline('image', '', src='/image.png', alt='awesome image'),
                        ' is here.',
                )
        ),
        (
                'このアイコン![アイコン](/image/icon.png)は良いですね。',
                (
                        'このアイコン',
                        create_inline('image', '', src='/image/icon.png', alt='アイコン'),
                        'は良いですね。'
                )
        ),
        (
                '最新の画像![画像](/画像.png)',
                (
                        '最新の画像',
                        create_inline('image', '', src='/画像.png', alt='画像'),
                        '',
                )
        ),
    ], ids=['head', 'both', 'tail'])
    def test_parse(self, text: str, expected: tuple[str, ImageInline, str]):
        # GIVEN
        sut = ImageParser()
        # WHEN
        actual = sut.parse(text)
        # THEN
        assert equal_for_inline_parse_result(actual, expected)
