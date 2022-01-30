from typing import TypeGuard
from a_pompom_markdown_parser.element.block import Block, PlainBlock, ParagraphBlock, QuoteBlock, ListBlock, ListItemBlock, ICodeBlock, \
    CodeBlock


class BlockConverter:
    """ 同種のBlock要素の集まりをHTMLと対応した形へ変換することを責務に持つ """

    def __init__(self):
        self._converter_list = [QuoteConverter(), ListConverter(), CodeBlockConverter()]

    def convert(self, blocks: list[Block]) -> list[Block]:
        """
        同種のBlock要素を1つに統合

        :param blocks: 統合対象となる同種のBlock群
        :return: 1つにまとめられたBlock要素
        """
        for converter in self._converter_list:
            if converter.is_target(blocks):
                # 「Python3.10-dev, PyCharm2021.2」の段階ではリストに対する型ガードが
                # 有効にならないようなので、型チェックを無効化
                # noinspection PyTypeChecker
                return [converter.convert(blocks)]

        return blocks


class IConverter:
    """ 変換処理のインタフェース """

    def is_target(self, blocks: list[Block]) -> TypeGuard[list[Block]]:
        """
        Block要素が変換対象か判定

        :param blocks: 対象Block要素群
        :return: True->変換対象 False->対象外
        """
        raise NotImplementedError()

    def convert(self, blocks: list[Block]) -> Block:
        """
        同種のBlock要素の集まりをHTMLタグを組み立てられる構造へ変換\n
        例えば引用要素であれば、1つの引用Block要素の子へ複数行からなる引用要素のテキストを持つ構造にできれば、\n
        開始タグ・終了タグの関係を容易に表現できる\n
        ビルダで変換してもよいが、ビルダの責務が大きくなりすぎるので、間にコンバータを介在させた

        :param blocks: 処理対象Block要素群
        :return: 根を元の要素・子をテキストと対応するBlock群としたBlock要素
        """
        raise NotImplementedError()


class QuoteConverter(IConverter):
    """ 引用要素を組み立てることを責務に持つ """

    # blockquoteタグ配下で描画されるため、要素は1階層分インデント
    INDENT_DEPTH = 1

    def is_target(self, blocks: list[Block]) -> TypeGuard[list[QuoteBlock]]:
        return all([isinstance(block, QuoteBlock) for block in blocks])

    def convert(self, blocks: list[QuoteBlock]) -> QuoteBlock:
        children = [ParagraphBlock(indent_depth=self.INDENT_DEPTH, children=block.children) for block in blocks]
        return QuoteBlock(children=children)


class ListConverter(IConverter):
    """ リスト要素を組み立てることを責務に持つ """

    def is_target(self, blocks: list[Block]) -> TypeGuard[list[ListBlock]]:
        return all([isinstance(block, ListBlock) for block in blocks])

    def convert(self, blocks: list[ListBlock]) -> ListBlock:
        # リストの子要素はliへ対応させるため、変換
        children = [ListItemBlock(children=block.children) for block in blocks]
        return ListBlock(children=children)


class CodeBlockConverter(IConverter):
    """ コードブロック要素を組み立てることを責務に持つ """

    # HTML上でスペースが含まれないよう、内部のインデント幅は0とする
    INDENT_DEPTH = 0

    def is_target(self, blocks: list[Block]) -> TypeGuard[list[Block]]:
        return all([isinstance(block, ICodeBlock) for block in blocks])

    def convert(self, blocks: list[ICodeBlock]) -> CodeBlock:
        """
        コードブロック・配下の要素をもとにHTMLのpre, codeタグの構造と対応したCodeBlock要素を生成

        :param blocks: ヘッダ(言語情報を含む)・コードを含むBlock群
        :return: 1つのBlockで統合したCodeBlock要素
        """

        language = self._get_code_language_from_header(blocks[0])
        # コードブロックはpre, codeタグの中でひとまとめに記述するため、統合
        children = [PlainBlock(indent_depth=self.INDENT_DEPTH, children=block.children)
                    for block in blocks[1:]]

        return CodeBlock(language=language, children=children)

    def _get_code_language_from_header(self, root_block: ICodeBlock) -> str:
        """
        先頭の要素からコードブロックのハイライト言語を取得

        :param root_block: 先頭のICodeBlock要素 「```<language>」で記述される
        :return: 「Python」のような、ハイライト言語文字列
        """

        # ダウンキャストの代用として型ガードを利用
        if not isinstance(root_block, CodeBlock):
            return ''

        # コードブロック要素は、
        # ```HTML
        # <div>code</div>
        # のように表現されるので、先頭は言語属性を持つ
        return root_block.language
