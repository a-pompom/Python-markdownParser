from typing import Generator, Literal

from a_pompom_markdown_parser.element.block import Block, ParseResult, CodeBlock, CodeChildBlock, TableOfContentsBlock
from a_pompom_markdown_parser.converter.block_converter import BlockConverter
from a_pompom_markdown_parser.converter.toc_converter import TocConverter


class Converter:
    """ 複数行におよぶBlock要素をHTMLタグと対応した形へ変換することを責務に持つ """

    def __init__(self):
        self._block_converter = BlockConverter()
        self._toc_converter = TocConverter()

    def convert(self, markdown_result: ParseResult) -> ParseResult:
        """
        ビルダの責務を小さくするため、マークダウンのパース結果をビルダが解釈しやすい形へ変換

        :param markdown_result: 変換対象のマークダウンパース結果
        :return: 変換結果
        """
        convert_result_content = []

        # 変換結果を同種のBlock単位へ分割してから変換
        # こうすることで、コンバータはただ入力を統合したものを出力するだけでよい
        for convert_target in split_to_convert_target(markdown_result.content):
            # 目次
            if self._toc_converter.is_target(convert_target):
                convert_result_content += self._toc_converter.convert(markdown_result)
                continue

            convert_result_content += self._block_converter.convert(convert_target)

        return ParseResult(content=convert_result_content)


def split_to_convert_target(blocks: list[Block]) -> Generator[list[Block], None, None]:
    """
    マークダウンの変換結果をコンバータの変換単位へ分割

    :param blocks: マークダウンの変換結果
    :return: ループで参照される度、1つのコンバータ変換単位を返却
    """

    # 開始・終了のインデックスでリストを分割していくことで、サブリストを生成し、毎回初期化するような
    # 煩雑な処理が要らなくなる
    start = 0
    end = 0

    for block in blocks:
        # 同種のブロックは同じコンバータで処理できるので、ひとまとめにする
        if block.is_same_type(blocks[start]):
            end += 1
            continue

        # Block要素が異なったタイミングで、リストの開始から終了インデックスまでの要素を
        # 返却すると、1種類のBlock要素で構成されるサブリストが得られる
        # コンバータはこれをまとめて処理していくことで、リスト・引用のような複数行に渡るBlock要素を
        # 統合できる
        yield blocks[start: end]
        start = end
        end += 1

    # 同じものが続いてループが終了した場合、ループ内のyield文だけではリストの中身全てを
    # 返却できないので、残りの要素を返却
    if start != end:
        yield blocks[start: end]
