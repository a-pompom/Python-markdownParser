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
