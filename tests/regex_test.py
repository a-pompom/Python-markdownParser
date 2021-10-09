import pytest

from app.regex import regex


class TestRegex:
    """ 正規表現の記法をもとに文字列の判定・抽出ができるか検証 """

    # テキストが記法を満たすか
    @pytest.mark.parametrize(('pattern', 'text', 'expected'), [
        (r'^#+ .*', '# this is heading', True),
        (r'^#+ .*', 'this is not heading', False),
        (r'.*`[^`]*`.*', 'quote like `this`', True),
    ])
    def test_contain(self, pattern: str, text: str, expected: bool):

        # GIVEN
        sut = regex
        # WHEN
        actual = sut.contain(pattern, text)
        # THEN
        assert actual == expected

    # キャプチャを取得
    @pytest.mark.parametrize(('pattern', 'text', 'groups', 'expected'), [
        (r'^(#+) (.*)', '# this is heading', [2], 'this is heading'),
        (r'(.*)\[(.*)\]\((.*)\)(.*)', 'that is [link](url) text', [2, 3], ('link', 'url'))
    ])
    def test_extract_from_group(self, pattern: str, text: str, groups: list[int], expected: list[str]):

        # GIVEN
        sut = regex
        # WHEN
        actual = sut.extract_from_group(pattern, text, groups)
        # THEN
        assert actual == expected
