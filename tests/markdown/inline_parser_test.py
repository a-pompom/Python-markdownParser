import pytest

from app.markdown.inline_parser import InlineParser, LinkParser, CodeParser, ImageParser
from app.element.inline import Inline


def assert_for_inline_parse_result(actual: tuple[str, Inline, str], expected: tuple[str, str, str]):
    """
    Inline要素のパース結果に対するAssertion

    :param actual: 実際に生成されたInline要素パース結果
    :param expected: 期待結果
    """

    actual_head, actual_inline, actual_tail = actual
    expected_head, expected_inline_repr, expected_tail = expected

    assert actual_head == expected_head
    # Inline要素は__repr__()により、文字列表現で比較
    assert repr(actual_inline) == expected_inline_repr
    assert actual_tail == expected_tail


class TestInlineParser:
    """ 行文字列からインライン記法を表現するInline要素を生成できるか検証 """

    # Inline要素生成
    @pytest.mark.parametrize(('text', 'expected'), [
        (
                'plain text',
                ['Plain: text=plain text']
        ),
        (
                'this is [google link](https://www.google.com/)',
                ['Plain: text=this is ', 'Link: text= google link, href=https://www.google.com/']
        )
    ], ids=['plain', 'link'])
    def test_parse(self, text: str, expected: list[str]):
        sut = InlineParser()
        actual = sut.parse(text)

        for actual_inline, expected_text in zip(actual, expected):
            repr(actual_inline) == expected_text


class TestLink:
    """ []()で表現されるリンク要素を検証 """

    # 記法が対象か
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            ('this is [link](url)', True),
            ('this is not link', False),
            ('[only link](http://www)', True),
            ('![image](http://www)', False)
        ],
        ids=['link text', 'not link', 'only link', 'image'])
    def test_target(self, text: str, expected: bool):
        sut = LinkParser()
        # WHEN
        actual = sut.is_target(text)
        # THEN
        assert actual == expected

    # 記法を解釈
    @pytest.mark.parametrize(
        ('link_text', 'expected'),
        [
            (
                    'normal[link](url)text',
                    ('normal', 'Link: text=link, href=url', 'text')
            ),
            (
                    '[link](http)',
                    ('', 'Link: text=link, href=http', '')
            ),
            (
                    '# heading [head link](https) text',
                    ('# heading ', 'Link: text=head link, href=https', ' text')
            ),
            (
                    'not ! image [link](url)text',
                    ('not ! image ', 'Link: text=link, href=url', 'text')
            ),
        ],
        ids=['normal link', 'only link', 'link with heading', 'not image'])
    def test_parse(self, link_text: str, expected: tuple[str, str, str]):
        # GIVEN
        sut = LinkParser()
        # WHEN
        actual = sut.parse(link_text)
        # THEN
        assert_for_inline_parse_result(actual, expected)


class TestCode:
    """ ``で表現されるコード要素を検証 """

    # 記法が対象か
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            ('Pythonのコメントは`#`で表現されます。', True),
            ('私はPythonが好きです', False),
        ],
        ids=['code', 'not code'])
    def test_target(self, text: str, expected: bool):
        # GIVEN
        sut = CodeParser()
        # WHEN
        actual = sut.is_target(text)
        # THEN
        assert actual == expected

    # 記法を解釈
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            (
                    '`//`でコメントを表現します。',
                    ('', 'Code: text=//', 'でコメントを表現します。')
            ),
            (
                    'JavaScriptの変数は`const`で宣言します。',
                    ('JavaScriptの変数は', 'Code: text=const', 'で宣言します。')
            ),
            (
                    'codeで終わります`。`',
                    ('codeで終わります', 'Code: text=。', '')
            ),
        ],
        ids=['no head', 'both', 'no tail'])
    def test_parse(self, text: str, expected: tuple[str, str, str]):
        # GIVEN
        sut = CodeParser()
        # WHEN
        actual = sut.parse(text)
        # THEN
        assert_for_inline_parse_result(actual, expected)


class TestImage:
    """ ![]()で表現される画像要素を検証 """

    # 対象判定
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            ('![画像](img.png)', True),
            ('[これはリンクです](https://www.google.com', False)
        ],
        ids=['target', 'not target'])
    def test_target(self, text: str, expected: bool):
        # GIVEN
        sut = ImageParser()
        # WHEN
        actual = sut.is_target(text)
        # THEN
        assert actual == expected

    # 記法を解釈
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            (
                    '![awesome image](/image.png) is here.',
                    ('', 'Image: src=/image.png, alt=awesome image', ' is here.')
            ),
            (
                    'このアイコン![アイコン](/image/icon.png)は良いですね。',
                    ('このアイコン', 'Image: src=/image/icon.png, alt=アイコン', 'は良いですね。')
            ),
            (
                    '最新の画像![画像](/画像.png)',
                    ('最新の画像', 'Image: src=/画像.png, alt=画像', '')
            ),
            (
                    '![画像](/画像.png)',
                    ('', 'Image: src=/画像.png, alt=画像', '')
            ),
        ],
        ids=['head', 'both', 'tail', 'inline_only'])
    def test_parse(self, text: str, expected: tuple[str, str, str]):
        # GIVEN
        sut = ImageParser()
        # WHEN
        actual = sut.parse(text)
        # THEN
        assert_for_inline_parse_result(actual, expected)
