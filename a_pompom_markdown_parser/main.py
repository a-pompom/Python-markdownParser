import os
import sys

from a_pompom_markdown_parser.markdown.parser import MarkdownParser
from a_pompom_markdown_parser.converter.converter import Converter
from a_pompom_markdown_parser.html.builder import HtmlBuilder

IN_AND_OUT_ARG_COUNT = 3


def validate_args():
    """
    コマンドライン引数を検証

    """

    # 引数の数
    if len(sys.argv) != IN_AND_OUT_ARG_COUNT:
        print('入力ファイルパス, 出力ファイルパスを指定してください。')
        sys.exit(1)

    # 入力ファイルがあるか
    if not os.path.exists(sys.argv[1]):
        print('入力ファイルが見つかりません。')
        sys.exit(1)

    # 出力ファイルが出力できるか
    try:
        f = open(sys.argv[2], 'w')
    except OSError:
        print(f'出力先: "{sys.argv[2]}"は無効です。')
        sys.exit(1)


def parse_md_to_html(in_file_path: str, out_file_path: str):
    """
    マークダウン→HTMLへ変換するメイン処理

    :param in_file_path: 入力マークダウンファイルパス
    :param out_file_path: 出力HTMLファイルパス
    """

    # マークダウンをパース
    with open(in_file_path, 'r') as f:
        markdown_parser = MarkdownParser()
        # 改行コードはHTMLを組み立てるときに制御するので、入力からは除外しておく
        markdown_parse_result = markdown_parser.parse(f.read().splitlines())

    # マークダウン・HTMLを中継
    converter = Converter()
    html_input = converter.convert(markdown_parse_result)

    # 変換結果HTMLを生成
    with open(out_file_path, 'w') as fw:
        html_builder = HtmlBuilder()
        fw.write(html_builder.build(html_input))


def parse_md_to_html_by_string(markdown_content: str) -> str:
    """
    文字列を入出力とし、マークダウン文字列をHTML文字列へパース

    :param markdown_content: マークダウン形式の文字列
    :return: HTML形式の文字列
    """
    markdown_parser = MarkdownParser()
    markdown_parse_result = markdown_parser.parse(markdown_content.splitlines())

    converter = Converter()
    html_input = converter.convert(markdown_parse_result)

    return HtmlBuilder().build(html_input)


def execute():
    """
    マークダウン文字列をHTMLへ変換
    """
    validate_args()
    parse_md_to_html(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    validate_args()
    parse_md_to_html(sys.argv[1], sys.argv[2])
