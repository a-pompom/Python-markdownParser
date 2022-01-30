import pytest

from a_pompom_markdown_parser.converter.converter import group_same_range_blocks
from a_pompom_markdown_parser.converter.block_converter import BlockConverter, QuoteConverter, ListConverter, CodeBlockConverter
from a_pompom_markdown_parser.markdown.parser import MarkdownParser


class TestBlockConverter:
    """
    Block要素のコンバータ
    本モジュールへの入力は、サブリスト構築関数により、同種のBlock要素のリストが渡される
    よって、テストでは同種のBlock要素のリストのみ検証
    """

    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (['今日はいい天気です。', '日記を終わります。'],
             ('[[Paragraph: indent_depth=0 | Child of Paragraph -> Plain: text=今日はいい天気です。], '
              '[Paragraph: indent_depth=0 | Child of Paragraph -> Plain: text=日記を終わります。]]')),

            (['> いい感じの言葉を', '> 引用します。'],
             ('[[Quote: | Child of Quote -> '
              '[Paragraph: indent_depth=1 | Child of Paragraph -> Plain: text=いい感じの言葉を]'
              ' | Child of Quote -> '
              '[Paragraph: indent_depth=1 | Child of Paragraph -> Plain: text=引用します。]]]')),

            (['* 1st', '* 2nd', '* 3rd'],
             ('[[List: indent_depth=0 | Child of List -> '
              '[ListItem: indent_depth=1 | Child of ListItem -> Plain: text=1st]'
              ' | Child of List -> '
              '[ListItem: indent_depth=1 | Child of ListItem -> Plain: text=2nd]'
              ' | Child of List -> '
              '[ListItem: indent_depth=1 | Child of ListItem -> Plain: text=3rd]]]')),
        ],
        ids=['plain', 'quote', 'list']
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
            (['> quote text'],
             '[Quote: | Child of Quote -> [Paragraph: indent_depth=1 | Child of Paragraph -> Plain: text=quote text]]'),
            (['> Pythonは', '> プログラミング言語です'],
             ('[Quote: | Child of Quote -> '
              '[Paragraph: indent_depth=1 | Child of Paragraph -> Plain: text=Pythonは] | Child of Quote -> '
              '[Paragraph: indent_depth=1 | Child of Paragraph -> Plain: text=プログラミング言語です]]')
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


class TestListConverter:
    """ リスト要素のコンバータ """

    # Block要素群が変換対象か
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (['* 1st element', '* 2nd element'], True),
            (['# Heading', 'Paragraph'], False),
        ],
        ids=['target', 'not target']
    )
    def test_is_target(self, lines: list[str], expected: bool):
        # GIVEN
        sut = ListConverter()
        markdown_result = MarkdownParser().parse(lines)
        # WHEN
        actual = sut.is_target(markdown_result.content)
        # THEN
        assert actual == expected

    # リスト・リスト子要素へ変換
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (['- method1'],
             ('[List: indent_depth=0 | Child of List -> '
              '[ListItem: indent_depth=1 | Child of ListItem -> Plain: text=method1]]')
             ),
            (['* item1', '* item2'],
             ('[List: indent_depth=0 | Child of List -> '
              '[ListItem: indent_depth=1 | Child of ListItem -> Plain: text=item1] | Child of List -> '
              '[ListItem: indent_depth=1 | Child of ListItem -> Plain: text=item2]]')
             ),
        ],
        ids=['single', 'multiple']
    )
    def test_convert(self, lines: list[str], expected: str):
        sut = ListConverter()
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


class TestCodeBlockConverter:
    """ コードブロック要素へ統合できるか """

    # 対象判定-対象
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (
                [
                    '```JavaScript',
                    'const i = 0;',
                    '// comment',
                    '```'
                ],
                True
            ),
        ],
    )
    def test_is_target_code_block(self, lines: list[str], expected: bool):
        # GIVEN
        sut = CodeBlockConverter()
        blocks = group_same_range_blocks(MarkdownParser().parse(lines).content)
        # WHEN
        actual = sut.is_target(blocks)
        # THEN
        assert actual == expected

    # 対象判定-対象外
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (['## Heading text', 'Plain text'], False),
        ]
    )
    def test_is_target_not_code_block(self, lines: list[str], expected: bool):
        # GIVEN
        sut = CodeBlockConverter()
        blocks = MarkdownParser().parse(lines).content
        # WHEN
        actual = sut.is_target(blocks)
        # THEN
        assert actual == expected

    # 1つのコードブロックへ統合されるか
    @pytest.mark.parametrize(
        ('lines', 'expected'),
        [
            (
                ['```Python', '# comment', 'instance = Klass()', '```'],
                ('[CodeBlock: language=Python | Child of CodeBlock -> '
                 '[Plain: indent_depth=0 | Child of Plain -> Plain: text=# comment]'
                 ' | Child of CodeBlock -> '
                 '[Plain: indent_depth=0 | Child of Plain -> Plain: text=instance = Klass()]]')
            ),
            (
                ['```', '## [参考](url)', '> 引用ここまで'],
                ('[CodeBlock: language= | Child of CodeBlock -> '
                 '[Plain: indent_depth=0 | Child of Plain -> Plain: text=## [参考](url)]'
                 ' | Child of CodeBlock -> '
                 '[Plain: indent_depth=0 | Child of Plain -> Plain: text=> 引用ここまで]]')
            ),
        ],
        ids=['code', 'not parsed']
    )
    def test_convert(self, lines: list[str], expected: str):
        # GIVEN
        sut = CodeBlockConverter()
        blocks = group_same_range_blocks(MarkdownParser().parse(lines).content)

        if not sut.is_target(blocks):
            assert False

        # WHEN
        # 「Python3.10-dev, PyCharm2021.2」の段階ではリストに対する型ガードが
        # 有効にならないようなので、型チェックを無効化
        # noinspection PyTypeChecker
        actual = sut.convert(blocks)
        # THEN
        assert repr(actual) == expected
