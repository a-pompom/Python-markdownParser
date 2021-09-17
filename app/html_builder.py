from app.markdown_parser import ParseResult, Inline, Block


class HtmlBuilder:
    """ HTML文字列の生成を責務に持つ """

    def __init__(self):
        pass

    def build(self, html_input: ParseResult) -> str:
        """
        入力をもとにHTML文字列を組み立て

        :param html_input: 入力要素 Block/Inlineからなるツリー要素
        :return: HTML文字列
        """

        html = ''

        for block in html_input.content:
            if isinstance(block, str):
                html = html + block
                continue

            if isinstance(block, Block):

                # TODO ネストしたブロックも扱えるようにしたい

                for child in block.children:

                    if isinstance(child, str):
                        html = html + child

        return html
