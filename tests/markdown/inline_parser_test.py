import pytest

from a_pompom_markdown_parser.element.inline import Inline, PlainInline, LinkInline, CodeInline, ImageInline
from a_pompom_markdown_parser.markdown.inline_parser import InlineParser, LinkParser, CodeParser, ImageParser


class TestInlineParser:
    """ 行文字列からインライン記法を表現するInline要素を生成できるか検証 """

    # Inline要素生成
    @pytest.mark.parametrize(('text', 'expected_list'), [
        (
            'plain text',
            [
                PlainInline(text='plain text')
            ]
        ),
        (
            'this is [google link](https://www.google.com/)',
            [
                PlainInline(text='this is '),
                LinkInline(href='https://www.google.com/', text='google link')
            ]
        )
    ], ids=['plain', 'link'])
    def test_parse(self, text: str, expected_list: list[Inline]):
        sut = InlineParser()
        actual_list = sut.parse(text)

        for actual, expected in zip(actual_list, expected_list):
            assert actual == expected


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

    # 記法に基づいて分離
    @pytest.mark.parametrize(
        ('link_text', 'expected'),
        [
            (
                'normal[link](url)text',
                ('normal', '[link](url)', 'text')
            ),
            (
                '[link](http)',
                ('', '[link](http)', '')
            ),
            (
                '# heading [head link](https) text',
                ('# heading ', '[head link](https)', ' text')
            ),
            (
                'not ! image [link](url)text',
                ('not ! image ', '[link](url)', 'text')
            ),
        ],
        ids=['normal link', 'only link', 'link with heading', 'not image'])
    def test_extract(self, link_text: str, expected: tuple[str, str, str]):
        sut = LinkParser()
        actual = sut.extract_text(link_text)
        assert actual == expected

    # 記法を解釈
    @pytest.mark.parametrize(
        ('link_text', 'expected'),
        [
            ('[link](url)', LinkInline(href='url', text='link')),
            ('[参考](http)', LinkInline(href='http', text='参考')),
        ],
        ids=['normal', 'full width'])
    def test_parse(self, link_text: str, expected: LinkInline):
        # GIVEN
        sut = LinkParser()
        # WHEN
        actual = sut.parse(link_text)
        # THEN
        assert actual == expected


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

    # 記法に基づいて分離
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            (
                '`//`でコメントを表現します。',
                ('', '`//`', 'でコメントを表現します。')
            ),
            (
                'JavaScriptの変数は`const`で宣言します。',
                ('JavaScriptの変数は', '`const`', 'で宣言します。')
            ),
            (
                'codeで終わります`。`',
                ('codeで終わります', '`。`', '')
            ),
        ],
        ids=['no head', 'both', 'no tail'])
    def test_extract(self, text: str, expected: tuple[str, str, str]):
        # GIVEN
        sut = CodeParser()
        # WHEN
        actual = sut.extract_text(text)
        # THEN
        assert actual == expected

    # 記法を解釈
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            ('`#Python comment`', CodeInline(text='#Python comment')),
            ('`素敵なコード`', CodeInline(text='素敵なコード')),
        ],
        ids=['normal', 'full width']
    )
    def test_parse(self, text: str, expected: CodeInline):
        # GIVEN
        sut = CodeParser()
        # WHEN
        actual = sut.parse(text)
        # THEN
        assert actual == expected


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

    # 記法に基づいて分離
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            (
                '![awesome image](/image.png) is here.',
                ('', '![awesome image](/image.png)', ' is here.')
            ),
            (
                'このアイコン![アイコン](/image/icon.png)は良いですね。',
                ('このアイコン', '![アイコン](/image/icon.png)', 'は良いですね。')
            ),
            (
                '最新の画像![画像](/画像.png)',
                ('最新の画像', '![画像](/画像.png)', '')
            ),
            (
                '![画像](/画像.png)',
                ('', '![画像](/画像.png)', '')
            ),
        ],
        ids=['head', 'both', 'tail', 'inline_only'])
    def test_extract(self, text: str, expected: tuple[str, str, str]):
        # GIVEN
        sut = ImageParser()
        # WHEN
        actual = sut.extract_text(text)
        # THEN
        assert actual == expected

    # 記法を解釈
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            ('![awesome image](/image.png)', ImageInline(src='/image.png', alt='awesome image', text='')),
            ('![画像](/image/例のアレ.png)', ImageInline(src='/image/例のアレ.png', alt='画像', text='')),
        ],
        ids=['normal', 'full width'])
    def test_parse(self, text: str, expected: ImageInline):
        # GIVEN
        sut = ImageParser()
        # WHEN
        actual = sut.parse(text)
        # THEN
        assert actual == expected
