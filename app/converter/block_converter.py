from typing import TypeGuard
from app.element.block import Block, PlainBlock, ParagraphBlock, QuoteBlock, ListBlock, ListItemBlock, CodeBlock


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

    # pre, codeタグ配下で描画されるため、要素は2階層分インデント
    INDENT_DEPTH = 2

    def is_target(self, blocks: list[Block]) -> TypeGuard[list[Block]]:
        return all([isinstance(block, CodeBlock) for block in blocks])

    def convert(self, blocks: list[CodeBlock]) -> CodeBlock:
        # コードブロックはpre, codeタグの中でひとまとめに記述するため、統合
        # 先頭要素はHTMLへ出力する必要がないので、除外
        # TODO 将来的には、```<language>の部分からhighlight jsのクラス属性を組み立てられるようにしたい
        children = [PlainBlock(indent_depth=self.INDENT_DEPTH, children=block.children)
                    for block in blocks[1:]]
        return CodeBlock(children=children)
