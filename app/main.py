import os
import sys

from app.markdown_parser import MarkdownParser
from app.converter import Converter
from app.html_builder import HtmlBuilder

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
        markdown_parse_result = markdown_parser.parse(f.readlines())

    # マークダウン・HTMLを中継
    converter = Converter()
    html_input = converter.convert(markdown_parse_result)

    # 変換結果HTMLを生成
    with open(out_file_path, 'w') as fw:
        html_builder = HtmlBuilder()
        fw.write(html_builder.build(html_input))


if __name__ == '__main__':
    validate_args()
    parse_md_to_html(sys.argv[1], sys.argv[2])
