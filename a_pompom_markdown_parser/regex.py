import re


class RegEx:
    """
    パース処理でよく使う正規表現関連処理のラップを責務に持つ
    """

    def contain(self, pattern: str, text: str) -> bool:
        """
        文字列がBlock要素のマークダウンの記法と合致するか判定

        :param pattern: 判定パターン 「# 」をヘッダとみなす、など
        :param text: 判定対象文字列
        :return: 合致 -> True, 合致しない -> False
        """
        return re.match(pattern, text) is not None

    def extract_from_group(self, pattern: str, text: str, groups: list[int]) -> list[str]:
        """
        記法・要素・属性などをテキストから抜き出す\n
        ex) r'(.*)`(.*)`(.*)', 'this is `quote` text', [1,2,3] -> ['this is ', 'quote', ' text']

        :param pattern: 判定パターン
        :param text: 抽出対象テキスト
        :param groups: 抜き出し対象インデックス
        :return: 抽出された文字列群
        """
        match: re.Match = re.match(pattern, text)
        # リストで指定されたインデックスをアンパックすることで、match.group()は抽出結果のタプルを返却
        return match.group(*groups)


regex = RegEx()
