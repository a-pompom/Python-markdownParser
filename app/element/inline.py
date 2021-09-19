import dataclasses
from app.element.style import Style


@dataclasses.dataclass
class Inline:
    """ aタグのようなインラインスタイルを保持 """
    style: Style
    text: str
