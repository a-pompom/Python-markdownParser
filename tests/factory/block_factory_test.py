import pytest

from tests.factory.block_factory import ListItemFactory, CodeChildBlockFactory


class TestListItemFactory:
    """ リストの子要素を生成できるか """

    # 単一
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            ('item1', '[ListItem: indent_depth=1 | Child of ListItem -> Plain: text=item1]'),
            ('要素1', '[ListItem: indent_depth=1 | Child of ListItem -> Plain: text=要素1]'),

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
             ['[ListItem: indent_depth=1 | Child of ListItem -> Plain: text=first]',
              '[ListItem: indent_depth=1 | Child of ListItem -> Plain: text=second]'])
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


class TestCodeChildBlockFactory:
    """ コードブロック子要素を生成できるか """

    # 単一
    @pytest.mark.parametrize(
        ('text', 'expected'),
        [
            ('', '[CodeChildBlock: | Child of CodeChildBlock -> Plain: text=]'),
            ('# plain heading', '[CodeChildBlock: | Child of CodeChildBlock -> Plain: text=# plain heading]'),
        ]
    )
    def test_single(self, text: str, expected: str):
        # GIVEN
        sut = CodeChildBlockFactory()
        # WHEN
        actual = sut.create_single_code_block(text)
        # THEN
        assert repr(actual) == expected

    # 複数
    @pytest.mark.parametrize(
        ('lines', 'expected_list'),
        [
            (
                    ['', '## Heading', '[link](url)'],
                    ['[CodeChildBlock: | Child of CodeChildBlock -> Plain: text=]',
                     '[CodeChildBlock: | Child of CodeChildBlock -> Plain: text=## Heading]',
                     '[CodeChildBlock: | Child of CodeChildBlock -> Plain: text=[link](url)]']
            )
        ]
    )
    def test_multiple(self, lines: list[str], expected_list: list[str]):
        # GIVEN
        sut = CodeChildBlockFactory()
        # WHEN
        actual_list = sut.create_multiple_code_block(lines)
        # THEn
        for actual, expected in zip(actual_list, expected_list):
            assert repr(actual) == expected
