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
                    ['> amazing quote text'],
                    '[Quote: | Child of Quote -> Plain: text=amazing quote text]'
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
        ids=['plain', 'heading', 'quote', 'code', 'image'])
    def test_parse(self, lines: list[str], expected: str):
        # GIVEN
        sut = MarkdownParser()
        # WHEN
        actual = sut.parse(lines)
        # THEN
        assert repr(actual) == expected

    # コードブロックのモードを制御できているか
    @pytest.mark.parametrize(
        ('lines', 'expected_list'),
        [
            (
                ['## 概要', '> すてきな概要です'],
                ['[Heading: size=2 | Child of Heading -> Plain: text=概要]',
                 '[Quote: | Child of Quote -> Plain: text=すてきな概要です]']
            ),

            (
                    ['### サンプルコード', '```', '# Pythonのコメント', '```', '#### 上はサンプルコードです'],
                    ['[Heading: size=3 | Child of Heading -> Plain: text=サンプルコード]',
                     '[CodeBlock: | Child of CodeBlock -> Plain: text=]',
                     '[Plain: | Child of Plain -> Plain: text=# Pythonのコメント]',
                     '[CodeBlock: | Child of CodeBlock -> Plain: text=]',
                     '[Heading: size=4 | Child of Heading -> Plain: text=上はサンプルコードです]']
            ),

            (
                    ['> コードが始まります', '```', '## コードを閉じるのを忘れました', '[まだコードです](url)'],
                    ['[Quote: | Child of Quote -> Plain: text=コードが始まります]',
                     '[CodeBlock: | Child of CodeBlock -> Plain: text=]',
                     '[Plain: | Child of Plain -> Plain: text=## コードを閉じるのを忘れました]',
                     '[Plain: | Child of Plain -> Plain: text=[まだコードです](url)]']
            ),
        ],
        ids=['no code block', 'code block with end symbol', 'no end symbol']
    )
    def test_parse_code_block_mode(self, lines: list[str], expected_list: list[str]):
        # GIVEN
        sut = MarkdownParser()
        # WHEN
        actual_result = sut.parse(lines)
        # THEN
        for actual, expected in zip(actual_result.content, expected_list):
            repr(actual) == expected
