def assert_that_text_file_content_is_same(expected_path: str, actual_path: str):
    """
    テキストファイルの中身が一致しているか検証

    :param expected_path: 期待結果テキストファイルのパス
    :param actual_path: 検証対象テキストファイルのパス
    """

    with open(expected_path, 'r') as expected:
        with open(actual_path, 'r') as actual:
            assert actual.read() == expected.read()
