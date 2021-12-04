import pytest

from tests.factory.block_factory import ListItemFactory


class TestListItemFactory:
    """ リストの子要素を生成できるか """

    # 単一
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            ('item1', '[ListItem: | Child of ListItem -> Plain: text=item1]'),
            ('要素1', '[ListItem: | Child of ListItem -> Plain: text=要素1]'),

        ],
        ids=['ascii', 'full width']
    )
    def test_single(self, text: str, expected: str):
        # GIVEN
        sut = ListItemFactory()
        # WHEN
        actual = sut.create_single_list_item(text)
        # THEN
        assert repr(actual) == expected

    # 複数
    @pytest.mark.parametrize(
        ('lines', 'expected_list'),
        [
            (['first', 'second'],
             ['[ListItem: | Child of ListItem -> Plain: text=first]',
              '[ListItem: | Child of ListItem -> Plain: text=second]'])
        ]
    )
    def test_multiple(self, lines: list[str], expected_list: list[str]):
        # GIVEN
        sut = ListItemFactory()
        # WHEN
        actual_list = sut.create_multiple_list_item(lines)
        # THEN
        for actual, expected in zip(actual_list, expected_list):
            assert repr(actual) == expected
