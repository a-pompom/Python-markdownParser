import pytest

from app.converter.converter import split_to_convert_target
from app.markdown.parser import MarkdownParser
from app.element.block import Block


# blockのリスト同士が同一とみなせるか判定
def assert_same_block_list(blocks: list[Block], expected_list: list[str]):
    actual = ''.join([repr(block) for block in blocks])
    expected = ''.join(expected_list)

    assert actual == expected


class TestSplitToConvertTarget:
    """ コンバータで処理できるようBlockのリストを種別ごとに分割 """

    # 1種類のBlock要素のみで構成
    @pytest.mark.parametrize(
        ('lines', 'expected_list'),
        [
            (
                    ['first plain text', 'second plain text'],
                    [['[Plain: | Child of Plain -> Plain: text=first plain text]',
                      '[Plain: | Child of Plain -> Plain: text=second plain text]']]
            ),
            (
                    ['> 私は昨日', '> こう言いました'],
                    [['[Quote: | Child of Quote -> Plain: text=私は昨日]',
                      '[Quote: | Child of Quote -> Plain: text=こう言いました]']]
            ),
        ],
        ids=['only plain', 'only block quote']
    )
    def test_only_single_type_block(self, lines: list[str], expected_list: list[list[str]]):
        # GIVEN
        sut = split_to_convert_target
        blocks = MarkdownParser().parse(lines).content

        # WHEN
        i = 0
        for convert_target in sut(blocks):
            # THEN
            assert_same_block_list(convert_target, expected_list[i])
            i += 1

    # 複数の種類のBlock要素が混在
    @pytest.mark.parametrize(
        ('lines', 'expected_list'),
        [
            (
                    ['# マークダウンとは', '> マークダウンとは', '> これです'],
                    [['[Heading: size=1 | Child of Heading -> Plain: text=マークダウンとは]'],
                     ['[Quote: | Child of Quote -> Plain: text=マークダウンとは]',
                      '[Quote: | Child of Quote -> Plain: text=これです]']
                     ]
            ),
            (
                    ['> 昨日私はこう言いました', '一日が過ぎました', '> 今日私はこう言いました', '> 帰りたい'],
                    [['[Quote: | Child of Quote -> Plain: text=昨日私はこう言いました]'],
                     ['[Plain: | Child of Plain -> Plain: text=一日が過ぎました]'],
                     ['[Quote: | Child of Quote -> Plain: text=今日私はこう言いました]',
                      '[Quote: | Child of Quote -> Plain: text=帰りたい]']
                     ]
            ),
        ],
        ids=['two type', 'two type between']
    )
    def test_multiple_type_blocks(self, lines: list[str], expected_list: list[list[str]]):
        # GIVEN
        sut = split_to_convert_target
        blocks = MarkdownParser().parse(lines).content

        # WHEN
        i = 0
        for convert_target in sut(blocks):
            # THEN
            assert_same_block_list(convert_target, expected_list[i])
            i += 1
