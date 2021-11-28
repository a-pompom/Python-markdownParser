import pytest

from app.converter.block_converter import BlockConverter, QuoteConverter
from app.markdown.parser import MarkdownParser


class TestBlockConverter:
    """
    Block要素のコンバータ
    本モジュールへの入力は、サブリスト構築関数により、同種のBlock要素のリストが渡される
    よって、テストでは同種のBlock要素のリストのみ検証
    サブリスト構築関数の出力を、今回の入力とすべきだと考えられるが、それはコンバータ本体が担保すべき観点なので、
    本モジュールはコンバータ以前の処理でつくられた入力を前提とする
    """

    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (['今日はいい天気です。', '日記を終わります。'],
             ('[[Plain: | Child of Plain -> Plain: text=今日はいい天気です。], '
              '[Plain: | Child of Plain -> Plain: text=日記を終わります。]]')),
            (['> いい感じの言葉を', '> 引用します。'],
             ('[[Quote: | Child of Quote -> '
              '[Plain: | Child of Plain -> Plain: text=いい感じの言葉を]'
              ' | Child of Quote -> '
              '[Plain: | Child of Plain -> Plain: text=引用します。]]]'))
        ],
        ids=['plain', 'quote']
    )
    def test_convert(self, lines: list[str], expected: str):
        # GIVEN
        sut = BlockConverter()
        markdown_result = MarkdownParser().parse(lines)
        # WHEN
        actual = sut.convert(markdown_result.content)
        # THEN
        assert repr(actual) == expected


class TestQuoteConverter:
    """ 引用要素のコンバータ """

    # Block要素群が変換対象か
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (['> quote text', '> 引用文です。'], True),
            (['plain text', 'plain 2nd line text'], False)
        ],
        ids=['target', 'not target']
    )
    def test_is_target(self, lines: list[str], expected: bool):
        # GIVEN
        markdown_result = MarkdownParser().parse(lines)
        sut = QuoteConverter()
        # WHEN
        actual = sut.is_target(markdown_result.content)
        # THEN
        assert actual == expected

    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (['> quote text'], '[Quote: | Child of Quote -> [Plain: | Child of Plain -> Plain: text=quote text]]'),
            (['> Pythonは', '> プログラミング言語です'],
             ('[Quote: | Child of Quote -> '
              '[Plain: | Child of Plain -> Plain: text=Pythonは] | Child of Quote -> '
              '[Plain: | Child of Plain -> Plain: text=プログラミング言語です]]')
             ),
        ],
        ids=['single', 'multiple']
    )
    def test_convert(self, lines: list[str], expected: str):
        # GIVEN
        sut = QuoteConverter()
        markdown_result = MarkdownParser().parse(lines)

        if not sut.is_target(markdown_result.content):
            assert False

        # WHEN
        # 「Python3.10-dev, PyCharm2021.2」の段階ではリストに対する型ガードが
        # 有効にならないようなので、型チェックを無効化
        # noinspection PyTypeChecker
        actual = sut.convert(markdown_result.content)
        # THEN
        assert repr(actual) == expected
