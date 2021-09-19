from app.markdown_parser import ParseResult
from app.element.block import Block
from app.element.inline import Inline


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
    print('Inline comparison')
    equality = (former.text == latter.text) and former.style == latter.style
    print(f'Inline equality: {equality}')

    return equality


def equal_for_block(former: Block, latter: Block) -> bool:
    """
    Block要素が等しいか検証

    :param former: 比較元
    :param latter: 比較先
    :return: 等しい -> True 等しくない -> False
    """

    print('Equality For Block')
    # 要素数
    if len(former.children) != len(latter.children):
        print(f'Children count is not same. former:{len(former.children)}, latter: {len(latter.children)}')
        return False
    print('Block children count is same')

    equality = True
    for former_child, latter_child in zip(former.children, latter.children):

        # テキスト
        if isinstance(former_child, str) and isinstance(latter_child, str):
            print('Child text comparison')
            equality = equality and (former_child == latter_child)
            print(f'Child text equality: {equality}')
            continue

        # Inline
        if isinstance(former_child, Inline) and isinstance(latter_child, Inline):
            print('Child inline comparison')
            equality = equality and equal_for_inline(former_child, latter_child)
            print(f'Child inline equality: {equality}')
            continue

        # Block
        if isinstance(former_child, Block) and isinstance(latter_child, Block):
            print('Child block comparison')
            equality = equality and equal_for_block(former_child, latter_child)
            print(f'Child block equality: {equality}')
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

    print('Compare ParserResult')
    # 要素数
    if len(former.content) != len(latter.content):
        return False
    print('Length is same')

    equality = True
    for former_block, latter_block in zip(former.content, latter.content):
        print('Block comparison')
        equality = equality and equal_for_block(former_block, latter_block)
        print(f'Block equality: {equality}')

    return equality
