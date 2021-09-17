from app.markdown_parser import Inline, Block, ParseResult


def assert_that_text_file_content_is_same(expected_path: str, actual_path: str):
    """
    テキストファイルの中身が一致しているか検証

    :param expected_path: 期待結果テキストファイルのパス
    :param actual_path: 検証対象テキストファイルのパス
    """

    with open(expected_path, 'r') as expected:
        with open(actual_path, 'r') as actual:
            assert actual.read() == expected.read()


def equal_for_inline(former: Inline, latter: Inline) -> bool:
    """
    Inline要素が等しいか検証

    :param former: 比較元
    :param latter: 比較先
    :return: 等しい -> True 等しくない -> False
    """
    return (former.text == latter.text) and former.style == latter.style


def equal_for_block(former: Block, latter: Block) -> bool:
    """
    Block要素が等しいか検証

    :param former: 比較元
    :param latter: 比較先
    :return: 等しい -> True 等しくない -> False
    """

    # 要素数
    if len(former.children) != len(latter.children):
        return False

    equality = True
    for former_child, latter_child in zip(former.children, latter.children):

        # テキスト
        if isinstance(former_child, str) and isinstance(latter_child, str):
            equality = equality and (former_child == latter_child)
            continue

        # Inline
        if isinstance(former_child, Inline) and isinstance(latter_child, Inline):
            equality = equality and equal_for_inline(former_child, latter_child)
            continue

        # Block
        if isinstance(former_child, Block) and isinstance(latter_child, Block):
            equality = equality and equal_for_block(former_child, latter_child)
            continue

        return False

    return equality


def equal_for_parse_result(former: ParseResult, latter: ParseResult) -> bool:
    """
    ParseResult要素が等しいか検証

    :param former: 比較元
    :param latter: 比較先
    :return: 等しい -> True 等しくない -> False
    """

    # 要素数
    if len(former.content) != len(latter.content):
        return False

    equality = True
    for former_block, latter_block in zip(former.content, latter.content):

        equality = equality and equal_for_block(former_block, latter_block)

    return equality

