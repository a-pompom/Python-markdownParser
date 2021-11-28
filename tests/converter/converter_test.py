import pytest

from app.converter.converter import Converter
from app.markdown.parser import MarkdownParser


class TestConverter:
    """ 複数行に渡る処理を統合、といったマークダウンとHTMLの橋渡し処理を検証 """

    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (['# 概要', 'これは概要です。'],
             ('[Heading: size=1 | Child of Heading -> Plain: text=概要] '
              '[Plain: | Child of Plain -> Plain: text=これは概要です。]')),

            (['> いい感じのことを', '> 言っているようです'],
             ('[Quote: | Child of Quote -> '
              '[Plain: | Child of Plain -> Plain: text=いい感じのことを]'
              ' | Child of Quote -> '
              '[Plain: | Child of Plain -> Plain: text=言っているようです]]')),

            (['## Pythonとは', '> Pythonとは', '> プログラミング言語です', '小休止', '> 再開'],
             ('[Heading: size=2 | Child of Heading -> Plain: text=Pythonとは] '
              '[Quote: | Child of Quote -> '
              '[Plain: | Child of Plain -> Plain: text=Pythonとは]'
              ' | Child of Quote -> '
              '[Plain: | Child of Plain -> Plain: text=プログラミング言語です]] '
              '[Plain: | Child of Plain -> Plain: text=小休止] '
              '[Quote: | Child of Quote -> '
              '[Plain: | Child of Plain -> Plain: text=再開]]'))

        ],
        ids=['no convert', 'only quote', 'mixed']
    )
    def test_convert(self, lines: list[str], expected: str):
        # GIVEN
        sut = Converter()
        markdown_result = MarkdownParser().parse(lines)
        # WHEN
        actual = sut.convert(markdown_result)
        # THEN
        assert repr(actual) == expected
