from typing import Generator, Literal

from a_pompom_markdown_parser.element.block import Block, ParseResult, CodeBlock, CodeChildBlock, TableOfContentsBlock
from a_pompom_markdown_parser.converter.block_converter import BlockConverter
from a_pompom_markdown_parser.converter.toc_converter import TocConverter


class Converter:
    """ 複数行におよぶBlock要素をHTMLタグと対応した形へ変換することを責務に持つ """

    def __init__(self):
        self._block_converter = BlockConverter()

    def convert(self, markdown_result: ParseResult) -> ParseResult:
        """
        ビルダの責務を小さくするため、マークダウンのパース結果をビルダが解釈しやすい形へ変換

        :param markdown_result: 変換対象のマークダウンパース結果
        :return: 変換結果
        """
        convert_result_content = []

        # コードブロックのような、記法の範囲内を同一とみなす要素をグループ化
        # より具体的には、同種のBlock要素へと変換することで、コンバータの処理単位としている
        grouped_markdown_result = group_same_range_blocks(markdown_result.content)

        # 変換結果を同種のBlock単位へ分割してから変換
        # こうすることで、コンバータはただ入力を統合したものを出力するだけでよい
        for convert_target in split_to_convert_target(grouped_markdown_result):
            # 目次
            if len(convert_target) == 1 and isinstance(convert_target[0], TableOfContentsBlock):
                convert_result_content += TocConverter().convert(markdown_result)
                continue

            convert_result_content += self._block_converter.convert(convert_target)

        return ParseResult(content=convert_result_content)


def group_same_range_blocks(blocks: list[Block]) -> list[Block]:
    """
    コードブロックのような間も同一のBlock要素とみなすものをグルーピング

    :param blocks: マークダウン変換結果
    :return: 範囲内を同一とみなすBlock要素がグループ化された結果
    """

    # 現在はどの範囲のBlock要素を処理しているか
    # モードに応じて範囲内のBlock要素をグループ化
    mode: Literal['Block'] | Literal['CodeBlock'] = 'Block'
    grouped_blocks = []

    for block in blocks:

        # コードブロック
        # 始点は、言語などの属性を後から参照するため、そのままグループ後のリストへ追加
        # 始点
        if mode == 'Block' and isinstance(block, CodeBlock):
            grouped_blocks.append(block)
            mode = 'CodeBlock'
            continue
        # 中間
        if mode == 'CodeBlock' and not isinstance(block, CodeBlock):
            grouped_blocks.append(CodeChildBlock(children=block.children))
            continue
        # 終点
        if mode == 'CodeBlock' and isinstance(block, CodeBlock):
            mode = 'Block'
            continue

        grouped_blocks.append(block)
    return grouped_blocks


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
