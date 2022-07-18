import os
import sys

from a_pompom_markdown_parser.markdown.parser import MarkdownParser
from a_pompom_markdown_parser.converter.converter import Converter
from a_pompom_markdown_parser.html.builder import HtmlBuilder

# コマンドライン引数定義
ARG_POS_IN_FILE = 1
ARG_POS_OUT_FILE = 2
IN_AND_OUT_ARG_COUNT = 3


class InvalidArgumentException(Exception):
    """ コマンドライン引数に問題があったことを表現 """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


def validate_args():
    """
    コマンドライン引数を検証
    """

    # 引数の数
    if len(sys.argv) != IN_AND_OUT_ARG_COUNT:
        raise InvalidArgumentException('入力ファイルパス, 出力ファイルパスを指定してください。')

    # 入力ファイルがあるか
    if not os.path.exists(sys.argv[ARG_POS_IN_FILE]):
        raise InvalidArgumentException('入力ファイルが見つかりません。')

    # 出力ファイルが出力できるか
    try:
        f = open(sys.argv[ARG_POS_OUT_FILE], 'w')
    except OSError:
        raise InvalidArgumentException(f'出力先: "{sys.argv[ARG_POS_OUT_FILE]}"は無効です。')


def parse_md_to_html(in_file_path: str, out_file_path: str):
    """
    マークダウン→HTMLへ変換するメイン処理

    :param in_file_path: 入力マークダウンファイルパス
    :param out_file_path: 出力HTMLファイルパス
    """

    # マークダウンをパース
    with open(in_file_path, 'r') as f:
        # 改行コードはHTMLを組み立てるときに制御するので、入力からは除外しておく
        markdown_parse_result = MarkdownParser().parse(f.read().splitlines())

    # マークダウン・HTMLを中継
    html_input = Converter().convert(markdown_parse_result)

    # 変換結果HTMLを生成
    with open(out_file_path, 'w') as fw:
        fw.write(HtmlBuilder().build(html_input))


def parse_md_to_html_by_string(markdown_content: str) -> str:
    """
    文字列を入出力とし、マークダウン文字列をHTML文字列へパース

    :param markdown_content: マークダウン形式の文字列
    :return: HTML形式の文字列
    """
    markdown_parse_result = MarkdownParser().parse(markdown_content.splitlines())

    html_input = Converter().convert(markdown_parse_result)

    return HtmlBuilder().build(html_input)


def execute():
    """
    マークダウン文字列をHTMLへ変換
    """
    try:
        validate_args()
    except InvalidArgumentException as e:
        print(e.message)
        sys.exit(1)

    parse_md_to_html(sys.argv[ARG_POS_IN_FILE], sys.argv[ARG_POS_OUT_FILE])


if __name__ == '__main__':
    execute()
