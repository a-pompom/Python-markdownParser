import pytest

from a_pompom_markdown_parser.element.block import Block, ParagraphBlock, HeadingBlock, QuoteBlock, ListBlock, \
    CodeBlock, HorizontalRuleBlock, TableOfContentsBlock
from a_pompom_markdown_parser.element.inline import PlainInline, LinkInline
from a_pompom_markdown_parser.markdown.inline_parser import InlineParser
from a_pompom_markdown_parser.markdown.block_parser import BlockParser, HeadingParser, QuoteParser, ListParser, \
    CodeBlockParser, HorizontalRuleParser, TableOfContentsParser


class TestBlockParser:
    """ 行文字列・Inline要素からInline要素を子に持つBlock要素が生成されるか検証 """

    # 行の分解
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            ('plain text', 'plain text'),
            ('### awesome heading', 'awesome heading'),
        ]
    )
    def test_extract_inline_text(self, text: str, expected: str):
        # GIVEN
        sut = BlockParser()
        # WHEN
        actual = sut.extract_inline_text(text)
        # THEN
        assert actual == expected

    # Block要素生成
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            (
                'plain text',
                ParagraphBlock(indent_depth=0, children=[
                    PlainInline(text='plain text')
                ])
            ),
            (
                '## awesome heading',
                HeadingBlock(size=2, children=[
                    PlainInline(text='awesome heading')
                ])
            ),
            (
                '> this is a pen.',
                QuoteBlock(children=[
                    PlainInline(text='this is a pen.')
                ])
            ),
            (
                '* 手順その1',
                ListBlock(indent_depth=0, children=[
                    PlainInline(text='手順その1')
                ])
            ),
            (
                '```JSX',
                CodeBlock(language='JSX', children=[
                    PlainInline(text='')
                ])
            ),
        ],
        ids=['plain', 'heading', 'quote', 'list', 'code_block'])
    def test_parse(self, text: str, expected: Block):
        # GIVEN
        sut = BlockParser()
        inline_parser = InlineParser()
        # WHEN
        children = inline_parser.parse(sut.extract_inline_text(text))
        actual = sut.parse(text, children)

        # THEN
        assert actual == expected


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

    # 記法を除いたテキストが得られるか
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            ('# 概要', '概要'),
            ('### Topic3', 'Topic3'),
        ]
    )
    def test_extract_text(self, text: str, expected: str):
        # GIVEN
        sut = HeadingParser()
        # WHEN
        actual = sut.extract_text(text)
        # THEN
        assert actual == expected

    # 記法の解釈
    @pytest.mark.parametrize(
        ('heading_text', 'expected'),
        [
            (
                '# this is heading',
                HeadingBlock(size=1, children=[
                    PlainInline(text='this is heading')
                ])
            ),
            (
                '###  3rd heading',
                HeadingBlock(size=3, children=[
                    PlainInline(text=' 3rd heading')
                ])
            ),
            (
                '## 2nd heading [link](url) text',
                HeadingBlock(size=2, children=[
                    PlainInline(text='2nd heading '),
                    LinkInline(href='url', text='link'),
                    PlainInline(text=' text')
                ])
            )
        ], ids=['1st heading', '3rd heading', '2nd heading with link'])
    def test_parse(self, heading_text: str, expected: HeadingBlock):
        # GIVEN
        sut = HeadingParser()
        inline_parser = InlineParser()
        children = inline_parser.parse(sut.extract_text(heading_text))
        # WHEN
        actual = sut.parse(heading_text, children)

        # THEN
        assert actual == expected


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

    # 記法を除いたテキストが得られるか
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
        ('text', 'expected'),
        [
            (
                '> awesome text',
                QuoteBlock(children=[
                    PlainInline(text='awesome text')
                ])
            ),
            (
                '> すごい発言',
                QuoteBlock(children=[
                    PlainInline(text='すごい発言')
                ])
            ),
        ],
        ids=['normal text', 'full width text']
    )
    def test_parse(self, text: str, expected: QuoteBlock):
        # GIVEN
        sut = QuoteParser()
        inline_parser = InlineParser()
        # WHEN
        actual = sut.parse(text, inline_parser.parse(sut.extract_text(text)))
        # THEN
        assert actual == expected


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
        ('text', 'expected'),
        [
            (
                '* first of all',
                ListBlock(indent_depth=0, children=[
                    PlainInline(text='first of all')
                ])
            ),
            (
                '- 1st',
                ListBlock(indent_depth=0, children=[
                    PlainInline(text='1st')
                ])
            ),
            (
                '- 最初',
                ListBlock(indent_depth=0, children=[
                    PlainInline(text='最初')
                ])
            ),
        ],
        ids=['* list', '- list', 'full width list']
    )
    def test_parse(self, text: str, expected: ListBlock):
        # GIVEN
        sut = ListParser()
        children = InlineParser().parse(sut.extract_text(text))
        # WHEN
        actual = sut.parse(text, children)
        # THEN
        assert actual == expected


class TestCodeBlock:
    """ ```で表現されるコードブロック要素"""

    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            ('```', True),
            ('```python', True),
            ('not code block', False),
        ],
        ids=['target for empty language', 'target', 'not target']
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
        [
            ('```', ''),
            ('```JavaScript', '')
        ]
    )
    def test_extract_text(self, text: str, expected: str):
        # GIVEN
        sut = CodeBlockParser()
        # WHEN
        actual = sut.extract_text(text)
        # THEN
        assert actual == expected

    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            (
                '```',
                CodeBlock(language='', children=[
                    PlainInline(text='')
                ])
            ),
            (
                '```HTML',
                CodeBlock(language='HTML', children=[
                    PlainInline(text='')
                ])
            ),
        ],
        ids=['empty language', 'some language']
    )
    def test_parse(self, text: str, expected: CodeBlock):
        # GIVEN
        sut = CodeBlockParser()
        children = InlineParser().parse(sut.extract_text(text))
        # WHEN
        actual = sut.parse(text, children)
        # THEN
        assert actual == expected


class TestHorizontalRule:
    """ ---で表現される水平線罫線要素を検証 """

    # 記法が対象か
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            ('---', True),
            ('罫線のつもりです', False),
        ],
        ids=['hr', 'not hr'])
    def test_target(self, text: str, expected: bool):
        # GIVEN
        sut = HorizontalRuleParser()
        # WHEN
        actual = sut.is_target(text)
        # THEN
        assert actual == expected

    # 記法に基づいて分離
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            (
                '---',
                ''
            ),
        ])
    def test_extract(self, text: str, expected: str):
        # GIVEN
        sut = HorizontalRuleParser()
        # WHEN
        actual = sut.extract_text(text)
        # THEN
        assert actual == expected

    # 記法を解釈
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            (
                '---',
                HorizontalRuleBlock(children=[
                    PlainInline(text='')
                ])
            )
        ]
    )
    def test_parse(self, text: str, expected: HorizontalRuleBlock):
        # GIVEN
        sut = HorizontalRuleParser()
        children = InlineParser().parse(sut.extract_text(text))
        # WHEN
        actual = sut.parse(text, children)
        # THEN
        assert actual == expected


class TestTableOfContents:
    """ [toc] で表現される目次要素を検証 """

    # 記法が対象か
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            ('[toc]', True),
            ('toc', False),
        ],
        ids=['toc', 'not toc'])
    def test_target(self, text: str, expected: bool):
        # GIVEN
        sut = TableOfContentsParser()
        # WHEN
        actual = sut.is_target(text)
        # THEN
        assert actual == expected

    # 記法に基づいて分離
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            (
                '[toc]',
                ''
            ),
        ])
    def test_extract(self, text: str, expected: str):
        # GIVEN
        sut = TableOfContentsParser()
        # WHEN
        actual = sut.extract_text(text)
        # THEN
        assert actual == expected

    # 記法を解釈できるか
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            (
                '[toc]',
                TableOfContentsBlock(children=[
                    PlainInline(text='')
                ])
            )
        ]
    )
    def test_parse(self, text: str, expected: TableOfContentsBlock):
        # GIVEN
        sut = TableOfContentsParser()
        children = InlineParser().parse(sut.extract_text(text))
        # WHEN
        actual = sut.parse(text, children)
        # THEN
        assert actual == expected
