import pytest

from a_pompom_markdown_parser.element.block import ListItemBlock
from a_pompom_markdown_parser.element.inline import PlainInline
from tests.factory.block_factory import ListItemFactory


class TestListItemFactory:
    """ リストの子要素を生成できるか """

    # 単一
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            (
                'item1',
                ListItemBlock(indent_depth=1, children=[
                    PlainInline(text='item1')
                ])
            ),
            (
                '要素1',
                ListItemBlock(indent_depth=1, children=[
                    PlainInline(text='要素1')
                ])
            ),
        ],
        ids=['ascii', 'full width']
    )
    def test_single(self, text: str, expected: ListItemBlock):
        # GIVEN
        sut = ListItemFactory()
        # WHEN
        actual = sut.create_single_list_item(text)
        # THEN
        assert actual == expected

    # 複数
    @pytest.mark.parametrize(
        ('lines', 'expected_list'),
        [
            (
                ['first', 'second'],
                [
                    ListItemBlock(indent_depth=1, children=[
                        PlainInline(text='first')
                    ]),
                    ListItemBlock(indent_depth=1, children=[
                        PlainInline(text='second')
                    ]),
                ]
            )
        ]
    )
    def test_multiple(self, lines: list[str], expected_list: list[ListItemBlock]):
        # GIVEN
        sut = ListItemFactory()
        # WHEN
        actual_list = sut.create_multiple_list_item(lines)
        # THEN
        for actual, expected in zip(actual_list, expected_list):
            assert actual == expected
