from app.markdown.parser import ParseResult
from app.element.block import Block, Children
from app.element.inline import Inline
from app.element.style import Style, Plain, Heading, Link, Code, Image


def assert_that_text_file_content_is_same(expected_path: str, actual_path: str):
    """
    テキストファイルの中身が一致しているか検証

    :param expected_path: 期待結果テキストファイルのパス
    :param actual_path: 検証対象テキストファイルのパス
    """

    with open(expected_path, 'r') as expected:
        with open(actual_path, 'r') as actual:
            assert actual.read() == expected.read()


# パース結果の等価判定
# 判定処理自体の妥当性は、各テストケースにより担保される
# これは、結局判定処理のテストコードを書いても、評価するためのオブジェクトを生成する作業が個別のテストケースと変わらないためである
def equal_for_inline(former: Inline, latter: Inline) -> bool:
    """
    Inline要素が等しいか検証

    :param former: 比較元
    :param latter: 比較先
    :return: 等しい -> True 等しくない -> False
    """
    print('Inline comparison')
    equality = (former.text == latter.text) and _equal_for_style(former.style, latter.style)
    print(f'Inline equality: {equality}')
    print(f'former: {former.text}')
    print(f'latter: {latter.text}')

    return equality


def equal_for_inline_parse_result(former: tuple[str, Inline, str], latter: tuple[str, Inline, str]) -> bool:
    """
    Inlineパーサの解釈結果が等しいか検証

    :param former: 比較元
    :param latter: 比較先
    :return: 等しい -> True 等しくない -> False
    """
    print(f'former: {former[0]}, {type(former[1])}, {former[2]}')
    print(f'latter: {latter[0]}, {type(latter[1])}, {latter[2]}')
    return former[0] == latter[0] and equal_for_inline(former[1], latter[1]) and former[2] == latter[2]


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

    # スタイル
    if not _equal_for_style(former.style, latter.style):
        print(
            f'Block style is not same. former:{former.style.__class__.__name__}, latter: {latter.style.__class__.__name__}')
        return False

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


def equal_for_children(former: Children, latter: Children):
    """
    Block要素の子が等しいか検証

    :param former: 比較元
    :param latter: 比較先
    :return: 等しい -> True 等しくない -> False
    """
    equality = True

    for former_child, latter_child in zip(former, latter):
        if isinstance(former_child, Block) and isinstance(latter_child, Block):
            equality = equality and equal_for_block(former_child, latter_child)
            continue

        if isinstance(former_child, Inline) and isinstance(latter_child, Inline):
            equality = equality and equal_for_inline(former_child, latter_child)
            continue

        # 型の不一致・想定外の型があったときは無条件で不一致とみなす
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


def _equal_for_style(former: Style, latter: Style) -> bool:
    """
    スタイル要素が同一か判定

    :param former: 比較元
    :param latter: 比較先
    :return: 等しい -> True 等しくない -> False
    """

    print('style comparison')
    # インスタンスの同一性
    if former.__class__.__name__ != latter.__class__.__name__:
        print('style is not same.')
        return False

    if isinstance(former, Plain):
        return True

    # Block
    # hタグ
    if isinstance(former, Heading) and isinstance(latter, Heading):
        print(f'Heading comparison former: {former.size}, latter: {latter.size}')
        return former.size == latter.size

    # Inline
    # aタグ
    if isinstance(former, Link) and isinstance(latter, Link):
        print(f'Link comparison former: {former.href}, latter: {latter.href}')
        return former.href == latter.href

    # codeタグ
    if isinstance(former, Code) and isinstance(latter, Code):
        return True

    # imgタグ
    if isinstance(former, Image) and isinstance(latter, Image):
        print('Image comparison')
        print(f'former.src: {former.src}, latter.src: {latter.src}')
        print(f'former.alt: {former.alt}, latter.alt: {latter.alt}')

        return former.src == latter.src and former.alt == latter.alt

    return True
