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
                '[Paragraph: indent_depth=0 | Child of Paragraph -> Plain: text=plain text]',
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
                ['* 1st element', '* 2nd element'],
                ('[List: indent_depth=0 | Child of List -> Plain: text=1st element] '
                 '[List: indent_depth=0 | Child of List -> Plain: text=2nd element]')
            ),

            (
                ['---'],
                '[HorizontalRule: | Child of HorizontalRule -> Plain: text=]'
            ),
        ],
        ids=['plain', 'heading', 'quote', 'list', 'horizontal rule'])
    def test_parse_block(self, lines: list[str], expected: str):
        # GIVEN
        sut = MarkdownParser()
        # WHEN
        actual = sut.parse(lines)
        # THEN
        assert repr(actual) == expected

    # Inline要素をパースできるか
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (
                ['[公式](https://docs.python.org/3/)を参照'],
                ('[Paragraph: indent_depth=0 | '
                 'Child of Paragraph -> Link: text=公式, href=https://docs.python.org/3/ | '
                 'Child of Paragraph -> Plain: text=を参照]')
            ),

            (
                ['記号`!`は否定を表現します。'],
                ('[Paragraph: indent_depth=0 | '
                 'Child of Paragraph -> Plain: text=記号 | '
                 'Child of Paragraph -> Code: text=! | '
                 'Child of Paragraph -> Plain: text=は否定を表現します。]')
            ),

            (
                ['![image](https://avatars.githubusercontent.com/u/43694794?v=4)'],
                ('[Paragraph: indent_depth=0 | '
                 'Child of Paragraph -> Image: src=https://avatars.githubusercontent.com/u/43694794?v=4, alt=image]')
            ),
        ],
        ids=['link', 'code', 'image']
    )
    def test_parse_inline(self, lines: list[str], expected: str):
        # GIVEN
        sut = MarkdownParser()
        # WHEN
        actual = sut.parse(lines)
        # THEN
        assert repr(actual) == expected

    # Block/Inline要素が混在した行をパースできるか
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (
                [
                    '## [Google](https://www.google.com/)とは',
                    '> `Google`の概要',
                ],
                ('[Heading: size=2 | Child of Heading -> '
                 'Link: text=Google, href=https://www.google.com/ | Child of Heading -> '
                 'Plain: text=とは] '
                 '[Quote: | Child of Quote -> '
                 'Code: text=Google | Child of Quote -> '
                 'Plain: text=の概要]')
            )
        ]
    )
    def test_parse_mixed(self, lines: list[str], expected: str):
        # GIVEN
        sut = MarkdownParser()
        # WHEN
        actual = sut.parse(lines)
        # THEN
        assert repr(actual) == expected

    # コードブロックのモードを制御できているか
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (
                ['## 概要', '> すてきな概要です'],
                ('[Heading: size=2 | Child of Heading -> Plain: text=概要] '
                 '[Quote: | Child of Quote -> Plain: text=すてきな概要です]')
            ),

            (
                ['### サンプルコード', '```Python', '# Pythonのコメント', '```', '#### 上はサンプルコードです'],
                ('[Heading: size=3 | Child of Heading -> Plain: text=サンプルコード] '
                 '[CodeBlock: language=Python | Child of CodeBlock -> Plain: text=] '
                 '[Plain: indent_depth=0 | Child of Plain -> Plain: text=# Pythonのコメント] '
                 '[CodeBlock: language= | Child of CodeBlock -> Plain: text=] '
                 '[Heading: size=4 | Child of Heading -> Plain: text=上はサンプルコードです]')
            ),

            (
                ['> コードが始まります', '```', '## コードを閉じるのを忘れました', '[まだコードです](url)'],
                ('[Quote: | Child of Quote -> Plain: text=コードが始まります] '
                 '[CodeBlock: language= | Child of CodeBlock -> Plain: text=] '
                 '[Plain: indent_depth=0 | Child of Plain -> Plain: text=## コードを閉じるのを忘れました] '
                 '[Plain: indent_depth=0 | Child of Plain -> Plain: text=[まだコードです](url)]')
            ),
        ],
        ids=['no code block', 'code block with end symbol', 'no end symbol']
    )
    def test_parse_code_block_mode(self, lines: list[str], expected: str):
        # GIVEN
        sut = MarkdownParser()
        # WHEN
        actual = sut.parse(lines)
        # THEN
        assert repr(actual) == expected
