from app.element.block import ListItemBlock, CodeBlock
from app.element.inline import PlainInline
from app.markdown.inline_parser import InlineParser


# Block要素のファクトリクラスは、コンバータでしか生成できないなど、インスタンスを
# 生成するのが困難なものに限定
# テスト済みのモジュールを介してテストデータを生成するよりもコストが掛かると判断した場合のみ、ファクトリクラスを定義する

class ListItemFactory:
    """ リストの子を表現するBlock要素を生成 """

    def create_single_list_item(self, text: str) -> ListItemBlock:
        """
        単一のリスト子要素を生成

        :param text: リスト子要素の文字列
        :return: ListItemBlock要素
        """
        return ListItemBlock(children=InlineParser().parse(text))

    def create_multiple_list_item(self, lines: list[str]) -> list[ListItemBlock]:
        """
        複数のリスト子要素を生成

        :param lines: 各リスト子要素の文字列を格納
        :return: ListItemBlock要素のリスト
        """
        return [ListItemBlock(children=InlineParser().parse(line)) for line in lines]


class CodeBlockFactory:
    """ コードブロックを表現するBlock要素を生成 """

    def create_single_code_block(self, text: str) -> CodeBlock:
        """
        単一のコードブロック要素を生成\n
        コードブロックの中では変換が必要ないので、Inline要素はパースしない

        :param text: コードブロック要素の文字列
        :return: CodeBlock要素
        """
        return CodeBlock(children=[PlainInline(text=text)])

    def create_multiple_code_block(self, lines: list[str]) -> list[CodeBlock]:
        """
        複数のコードブロック要素を生成\n
        コードブロックの中では変換が必要ないので、Inline要素はパースしない

        :param lines: 各コードブロック要素の文字列を格納
        :return: CodeBlock要素のリスト
        """
        return [CodeBlock(children=[PlainInline(text=line)]) for line in lines]
