from app.element.block import ListItemBlock, CodeChildBlock
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
