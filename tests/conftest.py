import sys
import os


def pytest_sessionstart(session):
    """
    前処理 相対importを解決するため、pathへアプリのディレクトリを追加

    """
    sys.path.append(f'{os.getcwd()}/../')
