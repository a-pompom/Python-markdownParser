from app.markdown_parser import ParseResult


class Converter:
    """ 変換結果をマークダウンの構造からHTMLの構造へマッピング"""

    def __init__(self):
        pass

    def convert(self, markdown_result: ParseResult) -> ParseResult:

        # TODO リストなど、マークダウン→HTMLで加工が必要なものを処理
        return markdown_result
