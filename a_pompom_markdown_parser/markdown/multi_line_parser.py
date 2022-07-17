from typing import Type

from a_pompom_markdown_parser.element.block import Block, CodeBlock, CodeChildBlock
from a_pompom_markdown_parser.regex import regex

from a_pompom_markdown_parser.markdown.block_parser import contain_block_notation
from a_pompom_markdown_parser.markdown.inline_parser import create_plain_inline

# パース処理で解釈した行数
# 呼び出し元をシンプルにするために、MultiLineParserは通常のパーサとあわせて呼び出される
# このとき、解釈した行数があれば、「通常のパーサはリストを1つ・MultiLineParserは返却された行数分」というルールでリストを走査でき、探索処理が書きやすくなる
ParseLength: Type = int
Parsed: Type = tuple[list[Block], ParseLength]


class MultiLineParser:
    """ 複数行を単位としたマークダウン要素をパースすることを責務に持つ """

    def __init__(self):
        self.parsers = [CodeBlockParser()]

    def is_target(self, line: str) -> bool:
        """
        現在行を参照し、複数行をまとめて解釈する必要があるか判定

        :param line: 現在参照しているテキスト行要素
        :return: パース対象-> True, 対象外-> False
        """
        for parser in self.parsers:
            if parser.is_target(line):
                return True

        return False

    def parse(self, lines: list[str]) -> Parsed:
        """
        現在行から複数行にわたるマークダウン要素を解釈

        :param lines: パース対象の複数行文字列
        :return: パース結果のBlock要素と、解釈した行数
        """

        for parser in self.parsers:

            if parser.is_target(lines[0]):
                parse_range = parser.extract_parse_range(lines)
                blocks = parser.parse(lines[0:parse_range + 1])

                return blocks, parse_range


class IParser:
    """ マークダウンで書かれた複数の行を解釈し、Block要素を生成することを責務に持つ """

    def is_target(self, markdown_text: str) -> bool:
        """
        マークダウンの行が現在参照しているパーサの処理対象であるか判定
        たとえば、```の場合、CodeBlockParserのみTrueを返し、それ以外はFalseを返す

        :param markdown_text: 判定対象行
        :return: パース対象 ->True パース対象でない -> False
        """
        raise NotImplementedError()

    def extract_parse_range(self, lines: list[str]) -> ParseLength:
        """
        複数行文字列のうち、パーサの扱う範囲を抽出

        :param lines: 抽出対象のテキスト群
        :return: 複数行文字列のパース行数
        """
        raise NotImplementedError()

    def parse(self, lines: list[str]) -> list[Block]:
        """
        複数行文字列を対象に、対応するBlock要素群を生成

        :param lines: 処理対象テキスト群
        :return 変換結果
        """
        raise NotImplementedError()


class CodeBlockParser(IParser):
    """ コードブロックを解釈することを責務に持つ """

    PATTERN = r'(```)(.*)'

    def is_target(self, markdown_text: str) -> bool:
        return contain_block_notation(self.PATTERN, markdown_text)

    def extract_parse_range(self, lines: list[str]) -> ParseLength:
        """
        コードブロックの開始「```」(先頭)から終了「```」までの要素数を抽出

        :param lines: コードブロックを含む複数行文字列
        :return: コードブロックの先頭から終了までの要素数
        """

        # 子を持たないものは終了要素「```」も持たないので打ち切り
        if self._has_no_children(lines):
            return len(lines)

        default_length = len(lines)
        code_children_lines = lines[1:]

        # コードブロックの終了「```」までがパース範囲となる
        for index, line in enumerate(code_children_lines, 1):
            if self.is_target(line):
                return index

        # 終了要素が無い場合、残りすべてがコードブロックに属することになる
        return default_length

    def _has_no_children(self, lines: list[str]) -> bool:
        """
        コードブロックが子を持たないか判定
        :param lines: コードブロックを含む、パース対象の複数行文字列
        :return: 子が存在-> True, 子がない->False
        """
        return len(lines) == 1

    def parse(self, lines: list[str]) -> list[Block]:
        """
        コードブロックの範囲をコード要素と、ブロック内部の子要素へ解釈

        :param lines: コードブロックを表現するマークダウン文字列
        :return: コードブロックとその子要素を表現するBlock
        """
        # ```Python
        # print('hello')
        # ```
        # それぞれが言語名・子要素・末尾に対応
        language_part, children_part, tail = lines[0], lines[1:-1], lines[-1]

        # コードブロックの末尾が「```」で閉じられたものでない場合、パース結果に残すべきなので子要素へ追加
        if not self.is_target(tail):
            children_part.append(tail)

        language = regex.extract_from_group(self.PATTERN, language_part, [2])
        # 複数行を対象としたパーサは、あくまでテキストをBlock要素に対応づけるのが責務である
        # 親子関係も表現していくとHTMLも意識することになり、Converterの責務まで担ってしまうのでここではchildrenプロパティによる親子関係を持たせない
        code_block = CodeBlock(language=language, children=[])
        # 末尾(```)はHTMLでは不要なのでパース結果に含めない
        return [code_block, *self._generate_code_children(children_part)]

    def _generate_code_children(self, children_part: list[str]) -> list[CodeChildBlock]:
        """
        コードブロックの子要素を表現するBlockを生成

        :param children_part: コードブロックの子に属する複数行文字列
        :return: コードブロックの子要素を表現するBlock
        """
        return [CodeChildBlock(children=[create_plain_inline(child_line)]) for child_line in children_part]
