import pytest
from a_pompom_markdown_parser.main import parse_md_to_html, parse_md_to_html_by_string
from a_pompom_markdown_parser.settings import setting

from tests.util_equality import assert_that_text_file_content_is_same


LINE_BREAK = setting['newline_code']

class TestMain:

    def test_plain(self):
        # GIVEN
        given_path = {
            'input': './template/markdown/plain.md',
            'output': './tmp/plain.html',
            'expected': './template/html/plain.html'
        }

        # WHEN
        parse_md_to_html(given_path['input'], given_path['output'])

        # THEN
        assert_that_text_file_content_is_same(given_path['expected'], given_path['output'])

    def test_block(self):
        text_path = {
            'input': './template/markdown/block.md',
            'output': './tmp/block.html',
            'expected': './template/html/block.html'
        }
        # WHEN
        parse_md_to_html(text_path['input'], text_path['output'])
        # THEN
        assert_that_text_file_content_is_same(text_path['expected'], text_path['output'])

    # inline
    def test_inline(self):
        # GIVEN
        text_path = {
            'input': './template/markdown/inline.md',
            'output': './tmp/inline.html',
            'expected': './template/html/inline.html'
        }
        # WHEN
        parse_md_to_html(text_path['input'], text_path['output'])
        # THEN
        assert_that_text_file_content_is_same(text_path['expected'], text_path['output'])

    # ブログ記事サンプル
    def test_sample_article(self):
        # GIVEN
        text_path = {
            'input': './template/markdown/sample_article.md',
            'output': './tmp/sample_article.html',
            'expected': './template/html/sample_article.html'
        }
        # WHEN
        parse_md_to_html(text_path['input'], text_path['output'])
        # THEN
        assert_that_text_file_content_is_same(text_path['expected'], text_path['output'])


class TestParseByString:
    """ 入出力を文字列とし、マークダウン要素をHTML要素へパースできるか検証 """

    # HTML文字列を組み立てられるか
    @pytest.mark.parametrize(
        ('markdown_content_path', 'expected_path'),
        [
            (
                './template/markdown/sample_article.md',
                './template/html/sample_article.html'
            )
        ]
    )
    def test_parse_by_string(self, markdown_content_path: str, expected_path: str):
        # GIVEN
        sut = parse_md_to_html_by_string
        # WHEN
        with open(markdown_content_path, 'r') as f:
            markdown_content = f.read()
            actual = sut(markdown_content)
            with open(expected_path, 'r') as f_expected:
                # THEN
                assert actual == f_expected.read()
