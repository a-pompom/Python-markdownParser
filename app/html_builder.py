class HtmlBuilder:
    """ HTML文字列の生成を責務に持つ """

    def __init__(self):
        self._text: list[str] = []

    @property
    def text(self):
        return ''.join(self._text)

    def append(self, line: str):
        """
        HTML文字列を追加

        :param line: 追加行文字列
        """

        self._text.append(line)
