import pytest

from app.converter.converter import Converter
from app.markdown.parser import MarkdownParser


class TestConverter:
    """ 複数行に渡る処理を統合、といったマークダウンとHTMLの橋渡し処理を検証 """

    # 変換無し
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (['# 概要', 'これは概要です。'],
             ('[Heading: size=1 | Child of Heading -> Plain: text=概要] '
              '[Plain: indent_depth=0 | Child of Plain -> Plain: text=これは概要です。]')),
        ]
    )
    def test_no_convert(self, lines: list[str], expected: str):
        # GIVEN
        sut = Converter()
        markdown_result = MarkdownParser().parse(lines)
        # WHEN
        actual = sut.convert(markdown_result)
        # THEN
        assert repr(actual) == expected

    # List要素を1つに統合できるか
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (['> いい感じのことを', '> 言っているようです'],
             ('[Quote: | Child of Quote -> '
              '[Plain: indent_depth=0 | Child of Plain -> Plain: text=いい感じのことを]'
              ' | Child of Quote -> '
              '[Plain: indent_depth=0 | Child of Plain -> Plain: text=言っているようです]]')),

            (['## Pythonとは', '> Pythonとは', '> プログラミング言語です', '小休止', '> 再開'],
             ('[Heading: size=2 | Child of Heading -> Plain: text=Pythonとは] '
              '[Quote: | Child of Quote -> '
              '[Plain: indent_depth=0 | Child of Plain -> Plain: text=Pythonとは]'
              ' | Child of Quote -> '
              '[Plain: indent_depth=0 | Child of Plain -> Plain: text=プログラミング言語です]] '
              '[Plain: indent_depth=0 | Child of Plain -> Plain: text=小休止] '
              '[Quote: | Child of Quote -> '
              '[Plain: indent_depth=0 | Child of Plain -> Plain: text=再開]]'))

        ],
        ids=['only one type element', 'mixed']
    )
    def test_convert_list(self, lines: list[str], expected: str):
        # GIVEN
        sut = Converter()
        markdown_result = MarkdownParser().parse(lines)
        # WHEN
        actual = sut.convert(markdown_result)
        # THEN
        assert repr(actual) == expected

    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (['```', '# comment, not heading', 'def func():', '```'],
             ('[CodeBlock: | Child of CodeBlock -> '
              '[Plain: indent_depth=2 | Child of Plain -> Plain: text=# comment, not heading]'
              ' | Child of CodeBlock -> '
              '[Plain: indent_depth=2 | Child of Plain -> Plain: text=def func():]]')),

            (['```', '[参考](https://)', '> コードは終わっていたはずです'],
             ('[CodeBlock: | Child of CodeBlock -> '
              '[Plain: indent_depth=2 | Child of Plain -> Plain: text=[参考](https://)]'
              ' | Child of CodeBlock -> '
              '[Plain: indent_depth=2 | Child of Plain -> Plain: text=> コードは終わっていたはずです]]')),
        ],
        ids=['has end', 'no end']
    )
    def test_convert_code_block(self, lines: list[str], expected: str):
        # GIVEN
        sut = Converter()
        markdown_result = MarkdownParser().parse(lines)
        # WHEN
        actual = sut.convert(markdown_result)
        # THEN
        assert repr(actual) == expected
