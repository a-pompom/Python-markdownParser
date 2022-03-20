from a_pompom_markdown_parser.regex import regex
from a_pompom_markdown_parser.element.block import Children, Block, PlainBlock, ParagraphBlock, HeadingBlock, \
    QuoteBlock, ListBlock, \
    CodeBlock, HorizontalRuleBlock, TableOfContentsBlock

# 正規表現のグループのうち、Blockの記法に属さない箇所のインデックス
# Inlineを解釈する処理をBlockとは独立させるために利用
INDEX_TEXT = 2


# 各パーサに共通する処理
# ミックスインや基底クラスの実装も考えられたが、継承関係はインタフェースに相当するものへ限定することで
# よりシンプルに解釈できるようにしたい よって、共通処理はモジュール上部へ関数で定義
def contain_block_notation(pattern: str, text: str) -> bool:
    """
    対象文字列がブロック要素の記法を含むか判定

    :param pattern: 判定対象パターン
    :param text: 対象文字列
    :return: 記法を含む ->True 記法を含まない -> False
    """
    return regex.contain(pattern, text)


def exclude_block_notation(pattern: str, text: str) -> str:
    """
    行を表現するテキストから、ブロック要素の記法を除外\n
    除外した結果をInline Parserへ渡すことで、Block/Inlineの処理を分離することができる

    :param pattern: 記法パターン
    :param text: 行テキスト
    :return: 行テキストからブロック要素の記法を除外した文字列
    """
    return regex.extract_from_group(pattern, text, [INDEX_TEXT])


class BlockParser:
    """ Block要素と対応するマークダウンの記法を解釈することを責務に持つ """

    def __init__(self):
        self.parsers: list[IParser] = [HeadingParser(), QuoteParser(), ListParser(), CodeBlockParser(),
                                       HorizontalRuleParser(), TableOfContentsParser()]

    def extract_inline_text(self, markdown_text: str) -> str:
        """
        処理対象行からBlock要素の記法を除外したものを抽出

        :param markdown_text: 対象行文字列
        :return: 対象行文字列からBlock要素の記法を除いたもの
        """

        for block_parser in self.parsers:
            if block_parser.is_target(markdown_text):
                return block_parser.extract_text(markdown_text)

        return markdown_text

    def parse(self, line: str, children: Children) -> Block:
        """
        マークダウンパーサを介して行をBlock要素へ変換

        :param line: 処理対象行
        :param children: 子要素
        :return: 変換結果のBlock要素
        """

        for parser in self.parsers:
            if parser.is_target(line):
                return parser.parse(line, children)

        return ParagraphBlock(children)


class IParser:
    """ マークダウンで書かれた行を解釈し、Block要素を生成することを責務に持つ """

    def is_target(self, markdown_text: str) -> bool:
        """
        マークダウンの行が現在参照しているパーサの処理対象であるか判定
        たとえば、`# Heading`の場合、HeadingParserのみTrueを返し、それ以外はFalseを返す

        :param markdown_text: 判定対象行
        :return: パース対象 ->True パース対象でない -> False
        """
        raise NotImplementedError()

    def extract_text(self, markdown_text: str) -> str:
        """
        Inline要素を組み立てるとき、Block要素の記法が関与しないよう切り出し
        これにより、Inline要素・Block要素それぞれのパース処理は、互いに関与せず、疎結合を保つことができる

        :param markdown_text: 対象行文字列
        :return: 対象行文字列からBlock要素の記法を抜いたもの
        """
        raise NotImplementedError()

    def parse(self, markdown_text: str, children: Children) -> Block:
        """
        マークダウンの行を解釈し、種類に応じたBlock要素を生成

        :param markdown_text: マークダウンの1行文字列
        :param children: Inlineパーサによって解釈された要素の集まり
        :return 変換結果
        """
        raise NotImplementedError()


class HeadingParser(IParser):
    """ ヘッダの解釈を責務に持つ"""
    PATTERN = '^(#+) (.*)'

    def is_target(self, markdown_text: str) -> bool:
        return contain_block_notation(self.PATTERN, markdown_text)

    def extract_text(self, markdown_text: str) -> str:
        return exclude_block_notation(self.PATTERN, markdown_text)

    def parse(self, markdown_text: str, children: Children) -> HeadingBlock:
        """
        ヘッダ行を解釈

        :param markdown_text: 処理対象行
        :param children: Inlineパーサによって解釈された要素の集まり
        :return: ヘッダを表すBlock要素
        """

        heading_style, text = regex.extract_from_group(self.PATTERN, markdown_text, [1, 2])

        return HeadingBlock(size=len(heading_style), children=children)


class QuoteParser(IParser):
    """ 引用要素の解釈を責務に持つ """
    PATTERN = r'(>) (.*)'

    def is_target(self, markdown_text: str) -> bool:
        return contain_block_notation(self.PATTERN, markdown_text)

    def extract_text(self, markdown_text: str) -> str:
        return exclude_block_notation(self.PATTERN, markdown_text)

    def parse(self, markdown_text: str, children: Children) -> QuoteBlock:
        """
        引用行を解釈

        :param markdown_text: 処理対象行
        :param children: Inlineパーサによって解釈された要素の集まり
        :return: 引用を表すBlock要素
        """
        return QuoteBlock(children)


class ListParser(IParser):
    """ リスト要素の解釈を責務に持つ """
    PATTERN = r'([\*\-]) (.*)'

    def is_target(self, markdown_text: str) -> bool:
        return contain_block_notation(self.PATTERN, markdown_text)

    def extract_text(self, markdown_text: str) -> str:
        return exclude_block_notation(self.PATTERN, markdown_text)

    def parse(self, markdown_text: str, children: Children) -> ListBlock:
        """
        リスト行を解釈

        :param markdown_text: 処理対象行
        :param children: Inlineパーサによって解釈された要素の集まり
        :return: リストを表すBlock要素
        """
        return ListBlock(children)


class CodeBlockParser(IParser):
    """ コードブロック要素の解釈を責務に持つ """
    PATTERN = r'(```)(.*)'

    def is_target(self, markdown_text: str) -> bool:
        return contain_block_notation(self.PATTERN, markdown_text)

    def extract_text(self, markdown_text: str) -> str:
        # コードブロックはInline要素へ文字列を渡す必要がないため、空文字を返却
        return ''

    def parse(self, markdown_text: str, children: Children) -> CodeBlock:
        """
        コードブロック行を解釈

        :param markdown_text: 処理対象行
        :param children: Inlineパーサによって解釈された要素の集まり
        :return: コードブロックを表すBlock要素
        """
        language = regex.extract_from_group(self.PATTERN, markdown_text, [2])

        return CodeBlock(language=language, children=children)


class HorizontalRuleParser(IParser):
    """ 水平罫線要素の解釈を責務に持つ """

    # ex) ---
    PATTERN = r'---'
    EXTRACT_PATTERN = r'(---)'

    def is_target(self, markdown_text: str) -> bool:
        return regex.contain(self.EXTRACT_PATTERN, markdown_text)

    def extract_text(self, markdown_text: str) -> str:
        # 水平罫線はInline要素へ文字列を渡す必要がないため、空文字を返却
        return ''

    def parse(self, markdown_text: str, children: Children) -> HorizontalRuleBlock:
        """
        水平罫線を表すBlock要素を生成

        :param markdown_text: 処理対象行
        :param children: Inlineパーサによって解釈された要素の集まり
        :return: 水平罫線を表すBlock要素
        """

        return HorizontalRuleBlock(children)


class TableOfContentsParser(IParser):
    """ 目次要素の解釈を責務に持つ """

    # ex) [toc]
    PATTERN = r'\[toc\]'
    EXTRACT_PATTERN = r'\[toc\]'

    def is_target(self, markdown_text: str) -> bool:
        return regex.contain(self.EXTRACT_PATTERN, markdown_text)

    def extract_text(self, markdown_text: str) -> str:
        # 目次要素はInline要素へ文字列を渡す必要がないため、空文字を返却
        return ''

    def parse(self, markdown_text: str, children: Children) -> TableOfContentsBlock:
        """
        目次を表すBlock要素を生成

        :param markdown_text: 処理対象行
        :param children: Inlineパーサによって解釈された要素の集まり
        :return: 目次を表すBlock要素
        """

        return TableOfContentsBlock(children)


# 特殊な要件によるBlockの生成
def create_plain_block(children: Children) -> PlainBlock:
    """
    パース処理無しで元の記法を保持したPlainなBlock要素を生成\n
    これは、コードブロックのような、元のマークダウンの記法をパースせず、そのまま残したいときに必要

    :param children: 子要素 元の行をすべて保持
    :return: パース処理無しで生成された元の行を表現するBlock要素
    """
    return PlainBlock(children)
