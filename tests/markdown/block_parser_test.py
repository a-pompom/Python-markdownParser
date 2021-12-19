import pytest

from app.markdown.inline_parser import InlineParser
from app.markdown.block_parser import BlockParser, HeadingParser, QuoteParser, ListParser, CodeBlockParser


class TestBlockParser:
    """ 行文字列・Inline要素からInline要素を子に持つBlock要素が生成されるか検証 """

    # 行の分解
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            ('plain text', 'plain text'),
            ('### awesome heading', 'awesome heading'),
        ],
        ids=['plain', 'heading'])
    def test_extract_inline_text(self, text: str, expected: str):
        # GIVEN
        sut = BlockParser()
        # WHEN
        actual = sut.extract_inline_text(text)
        # THEN
        assert actual == expected

    # Block要素生成
    @pytest.mark.parametrize(
        ('text', 'child_text', 'expected'),
        [
            (
                    'plain text',
                    'plain text',
                    '[Paragraph: indent_depth=0 | Child of Paragraph -> Plain: text=plain text]'
            ),
            (
                    '## awesome heading',
                    'awesome heading',
                    '[Heading: size=2 | Child of Heading -> Plain: text=awesome heading]'
            ),
            (
                    '> this is a pen.',
                    'this is a pen.',
                    '[Quote: | Child of Quote -> Plain: text=this is a pen.]'
            ),
            (
                    '* 手順その1',
                    '手順その1',
                    '[List: indent_depth=0 | Child of List -> Plain: text=手順その1]'
            ),
            (
                    '```',
                    '',
                    '[CodeBlock: | Child of CodeBlock -> Plain: text=]'
            ),
        ],
        ids=['plain', 'heading', 'quote', 'list', 'code_block'])
    def test_parse(self, text: str, child_text: str, expected: str):
        # GIVEN
        sut = BlockParser()
        inline_parser = InlineParser()
        # WHEN
        children = inline_parser.parse(child_text)
        actual = sut.parse(text, children)

        # THEN
        assert repr(actual) == expected


class TestHeading:
    """ #で表現されるヘッダ要素 """

    # 記法が対象か
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            ('# this is heading', True),
            ('this is not heading', False),
            ('###Without space', False),
            ('＃FullWidth character', False)
        ],
        ids=['heading', 'not heading', 'no space', 'FullWidth'])
    def test_target(self, text: str, expected: bool):
        # GIVEN
        sut = HeadingParser()
        # WHEN
        actual = sut.is_target(text)
        # THEN
        assert actual == expected

    # 記法の解釈
    @pytest.mark.parametrize(
        ('heading_text', 'child_text', 'expected'),
        [
            (
                    '# this is heading',
                    'this is heading',
                    '[Heading: size=1 | Child of Heading -> Plain: text=this is heading]'
            ),
            (
                    '###  3rd heading',
                    ' 3rd heading',
                    '[Heading: size=3 | Child of Heading -> Plain: text= 3rd heading]'
            ),
            (
                    '## 2nd heading [link](url) text',
                    '2nd heading [link](url) text',
                    ('[Heading: size=2 | '
                     'Child of Heading -> Plain: text=2nd heading  | '
                     'Child of Heading -> Link: text=link, href=url | '
                     'Child of Heading -> Plain: text= text]')
            )
        ], ids=['1st heading', '3rd heading', '2nd heading with link'])
    def test_parse(self, heading_text: str, child_text: str, expected: str):
        # GIVEN
        sut = HeadingParser()
        inline_parser = InlineParser()
        # WHEN
        children = inline_parser.parse(child_text)
        actual = sut.parse(heading_text, children)

        # THEN
        assert repr(actual) == expected


class TestQuote:
    """ >で表現される引用要素 """

    # 記法が対象か
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            ('> なんかいい感じの引用', True),
            ('>no space', False),
            ('plain text', False),

        ],
        ids=['target', 'no space', 'plain text']
    )
    def test_target(self, text: str, expected: bool):
        # GIVEN
        sut = QuoteParser()
        # WHEN
        actual = sut.is_target(text)
        # THEN
        assert actual == expected

    # 記法に関連しないテキストの切り出し
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            ('> Quote text', 'Quote text'),
            ('> なんかいい感じの発言', 'なんかいい感じの発言'),

        ],
        ids=['text', 'full width text']
    )
    def test_extract(self, text: str, expected: str):
        # GIVEN
        sut = QuoteParser()
        # WHEN
        actual = sut.extract_text(text)
        # THEN
        assert actual == expected

    # 記法の解釈
    @pytest.mark.parametrize(
        ('text', 'child_text', 'expected'),
        [
            (
                    '> awesome text',
                    'awesome text',
                    '[Quote: | Child of Quote -> Plain: text=awesome text]'
            ),
            (
                    '> すごい発言',
                    'すごい発言',
                    '[Quote: | Child of Quote -> Plain: text=すごい発言]'
            ),
        ],
        ids=['normal text', 'full width text']
    )
    def test_parse(self, text: str, child_text: str, expected: str):
        # GIVEN
        sut = QuoteParser()
        inline_parser = InlineParser()
        # WHEN
        actual = sut.parse(text, inline_parser.parse(child_text))
        # THEN
        assert repr(actual) == expected


class TestList:
    """ */- で表現されるリスト要素 """

    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            ('* 1つ目', True),
            ('- その1', True),
            ('Plain text', False)
        ],
        ids=['target *', 'target -', 'not target']
    )
    def test_is_target(self, text: str, expected: bool):
        # GIVEN
        sut = ListParser()
        # WHEN
        actual = sut.is_target(text)
        # THEN
        assert actual == expected

    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            ('* first thing', 'first thing'),
            ('- awesome list', 'awesome list'),
            ('* 1つ目の理由', '1つ目の理由')

        ],
        ids=['* text', '- text', 'full width text']
    )
    def test_extract_text(self, text: str, expected: str):
        # GIVEN
        sut = ListParser()
        # WHEN
        actual = sut.extract_text(text)
        # THEN
        assert actual == expected

    @pytest.mark.parametrize(
        ('text', 'child_text', 'expected'),
        [
            ('* first of all', 'first of all', '[List: indent_depth=0 | Child of List -> Plain: text=first of all]'),
            ('- 1st', '1st', '[List: indent_depth=0 | Child of List -> Plain: text=1st]'),
            ('- 最初', '最初', '[List: indent_depth=0 | Child of List -> Plain: text=最初]'),
        ],
        ids=['* list', '- list', 'full width list']
    )
    def test_parse(self, text: str, child_text: str, expected: str):
        # GIVEN
        sut = ListParser()
        children = InlineParser().parse(child_text)
        # WHEN
        actual = sut.parse(text, children)
        # THEN
        assert repr(actual) == expected


class TestCodeBlock:
    """ ```で表現されるコードブロック要素"""

    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            ('```', True),
            ('not code block', False),
        ],
        ids=['target', 'not target']
    )
    def test_is_target(self, text: str, expected: bool):
        # GIVEN
        sut = CodeBlockParser()
        # WHEN
        actual = sut.is_target(text)
        # THEN
        assert actual == expected

    @pytest.mark.parametrize(
        ('text', 'expected'),
        [('```', '')]
    )
    def test_extract_text(self, text: str, expected: str):
        # GIVEN
        sut = CodeBlockParser()
        # WHEN
        actual = sut.extract_text(text)
        # THEN
        assert actual == expected

    @pytest.mark.parametrize(
        ('text', 'child_text', 'expected'),
        [('```', '', '[CodeBlock: | Child of CodeBlock -> Plain: text=]')]
    )
    def test_parse(self, text: str, child_text: str, expected: str):
        # GIVEN
        sut = CodeBlockParser()
        children = InlineParser().parse(child_text)
        # WHEN
        actual = sut.parse(text, children)
        # THEN
        assert repr(actual) == expected
