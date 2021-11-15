import pytest

from app.markdown.parser import MarkdownParser


class TestMarkdownParser:
    """ Block/Inlineをまとめて扱い、行文字列からマークダウンのパース結果を生成する機能を検証 """

    # パース結果
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (
                    ['plain text'],
                    '[Plain: | Child of Plain -> Plain: text=plain text]',
            ),
            (
                    ['## awesome heading'],
                    '[Heading: size=2 | Child of Heading -> Plain: text=awesome heading]'
            ),
            (
                    ['記号`!`は否定を表現します。'],
                    ('[Plain: | '
                     'Child of Plain -> Plain: text=記号 | '
                     'Child of Plain -> Code: text=! | '
                     'Child of Plain -> Plain: text=は否定を表現します。]')
            ),
            (
                    ['![image](https://avatars.githubusercontent.com/u/43694794?v=4)'],
                    ('[Plain: | '
                     'Child of Plain -> Image: src=https://avatars.githubusercontent.com/u/43694794?v=4, alt=image]')
            ),
        ],
        ids=['plain', 'heading', 'code', 'image'])
    def test_parse(self, lines: list[str], expected: str):
        # GIVEN
        sut = MarkdownParser()
        # WHEN
        actual = sut.parse(lines)
        # THEN
        assert repr(actual) == expected
