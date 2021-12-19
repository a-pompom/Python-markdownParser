from app.main import parse_md_to_html

from tests.util_equality import assert_that_text_file_content_is_same


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
