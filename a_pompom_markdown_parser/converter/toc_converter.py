import dataclasses
from typing import Generator

from a_pompom_markdown_parser.element.block import ParseResult, HeadingBlock, ListBlock, ListItemBlock, Block, \
    TableOfContentsBlock
from a_pompom_markdown_parser.element.inline import LinkInline
from a_pompom_markdown_parser.block_utility import get_text_from_block


@dataclasses.dataclass
class TocNode:
    """ 目次の構造と対応する木のノードを表現することを責務に持つ """

    # 階層
    depth: int
    # 目次テキスト
    text: str

    # 子要素
    # 目次の構造を表せるよう自身の型のみに限定
    children: list['TocNode']

    # 等価比較
    def __eq__(self, other: 'TocNode'):
        # 階層・テキストいずれかが異なる場合は不一致
        if self.depth != other.depth or self.text != other.text:
            return False

        # 子ノードの要素数が異なる場合は不一致
        if len(self.children) != len(other.children):
            return False

        # 子ノードも同様に一致するか検証
        for left_child, right_child in zip(self.children, other.children):
            return left_child.__eq__(right_child)

        return True


class TocNodeTreeGenerator:
    """ 目次の構造を表現する木をつくり出すことを責務に持つ """

    def generate(self, header_list: list[HeadingBlock]) -> list[TocNode]:
        """
        目次の構造を表現する木を生成

        :param header_list: マークダウンの文書から目次に関わるヘッダのみを抽出したリスト
        :return: 目次の構造そのものを木で表現したオブジェクト 目次は複数の根を持つ可能性があることから、リスト型とした
        """

        # 木を構成する要素が空
        if len(header_list) == 0:
            return []

        # 子を追加しながら目次構造の木を生成
        return [self._generate(partial_header_list)
                for partial_header_list in self._split_per_root(header_list)]

    def _split_per_root(self, header_list: list[HeadingBlock]) -> Generator[
        list[HeadingBlock], None, None]:
        """
        目次の親を持たない要素単位で入力を分割\n
        親を持たない、すなわち根となる要素は分けて処理した方が見通しが良くなるので、1つの木を単位として処理するためのジェネレータを定義
        :param header_list: 目次のもととなるヘッダのリスト
        :return: 目次の構造の1つの木
        """

        root_index = 0
        # 根を単位に目次の構成要素を分割
        for current, header in enumerate(header_list):
            # 目次は同階層の場合、別の木で構築されることから、自身以上の階層を別の木とみなす
            is_another_root = root_index != current and header_list[root_index].size >= header.size
            if is_another_root:
                yield header_list[root_index:current]

                # 新しい木の根
                root_index = current

        yield header_list[root_index:]
        return

    def _generate(self, header_list: list[HeadingBlock]) -> TocNode:
        """
        目次構造の木を表現するTocNodeを生成

        :param header_list: 目次の構成要素となるヘッダBlockからなるリスト
        :return: 最も階層の浅いノードを根とするTocNodeのツリー
        """

        # 木の根は位置が自明であるため、探索対象から除いておく
        root = TocNode(depth=header_list[0].size, children=[], text=get_text_from_block(header_list[0]))
        # 木に子が存在しない
        is_only_root = len(header_list) == 1
        if is_only_root:
            return root

        # ノードを加える木の位置を探索
        child_header_list = header_list[1:]
        for header in child_header_list:
            self._find_appropriate_child_position(root, header).children.append(
                TocNode(depth=header.size, children=[], text=get_text_from_block(header))
            )

        return root

    def _find_appropriate_child_position(self, root: TocNode, header: HeadingBlock) -> TocNode:
        """
        目次の子要素として、木のどこに配置すべきか探索

        :param root: 木の根となるノード
        :param header: 位置を決めたいノードの元となる要素
        :return: 対象要素が子として属すべき親ノード
        """

        current = root
        while True:

            # 子を持たない、あるいは同階層の子が既に存在する場合は、現在参照しているノードの子とする
            # こうすることで、親より階層の深いものは子となり、同階層のものは兄弟ノードとなるルールを満たすことができる
            # つまり、目次の木を満たすための条件に合致する
            is_tail = len(current.children) == 0
            has_sibling = not is_tail and current.children[0].depth == header.size

            if is_tail or has_sibling:
                return current

            # 目次において、3章3節の次に3章2節1項が書かれることはない
            # つまり、階層が深くなる場合は最後に定義されたものの子にしかなり得ないので、末尾の子へ参照を切り替える
            current = current.children[len(current.children) - 1]


class TocGenerator:
    """ 目次を表現するBlock要素をつくり出すことを責務に持つ """

    # 目次を表現するul/liのインデント初期値
    ROOT_UL_INDENT = 0
    ROOT_LI_INDENT = 1
    # 次のul/liは間にli/ulを挟むため、インデント幅の増分は2となる
    INDENT_INCREMENT = 2

    def generate(self, toc_node_list: list[TocNode]) -> list[ListBlock]:
        """
        目次を表現するul/li Block要素を組み立てる

        :param toc_node_list: 目次構造を表現するTocNodeのリスト
        :return: 目次を表現するul/li Block要素のリスト
        """

        toc = []

        for toc_node in toc_node_list:
            # 根となるノードは、自身のテキストを表現するli・子を保持するためのliがそれぞれ必要
            root = ListBlock(indent_depth=self.ROOT_UL_INDENT, children=[
                self._convert_toc_text_to_li(toc_node, self.ROOT_LI_INDENT)])
            # 子が空
            if len(toc_node.children) == 0:
                toc.append(root)
                continue

            # 次のulはliを挟んだ後のものなので、増分を加算
            child_ul_indent = self.ROOT_UL_INDENT + self.INDENT_INCREMENT
            # liはroot.childrenと同階層なので増分はなし
            child_li_indent = self.ROOT_LI_INDENT

            root.children.append(self._generate_children(toc_node.children, child_li_indent, child_ul_indent))
            toc.append(root)

        return toc

    def _generate_children(self, children: list[TocNode], li_indent: int, ul_indent: int) -> ListItemBlock:
        """
        目次を表現するul/liツリーの子をTocNodeから構築

        :param children: TocNodeの子要素
        :param li_indent: li要素のインデント幅
        :param ul_indent: ネストしたul要素のインデント幅
        :return: ul/li要素を表現するBlockからなる目次の部分木
        """

        # ul/liがネストする場合、liが子にulを持つ
        wrapper = ListItemBlock(indent_depth=li_indent, children=[
            ListBlock(indent_depth=ul_indent, children=[])
        ])
        # 目次の末尾へTocNodeを変換した結果を追加
        wrapper_leaf = wrapper.children[0].children
        child_li_indent = li_indent + self.INDENT_INCREMENT
        child_ul_indent = ul_indent + self.INDENT_INCREMENT

        for child in children:

            # 子を持たない場合はそれ以上子が増えることはないので、終端となる
            if len(child.children) == 0:
                wrapper_leaf.append(self._convert_toc_text_to_li(child, child_li_indent))
                continue

            # 子を持つ場合は、目次のテキストを表現するliと、子構造を表現するli/ulを追加
            wrapper_leaf.append(self._convert_toc_text_to_li(child, child_li_indent))
            wrapper_leaf.append(self._generate_children(child.children, child_li_indent, child_ul_indent))

        return wrapper

    def _convert_toc_text_to_li(self, toc_node: TocNode, li_indent: int) -> ListItemBlock:
        """
        目次ノードのテキスト属性からli + aタグ要素へ変換

        :param toc_node: 目次ノード
        :param li_indent: インデント幅
        :return: 目次HTMLのツリーへ加えることができる、li + aタグで表現されたブロック
        """
        anchor = LinkInline(text=toc_node.text, href=f'#{toc_node.text}')
        return ListItemBlock(indent_depth=li_indent, children=[anchor])


class TocConverter:
    """ 目次の構成要素となるHeading Blockから目次の実体と対応するBlock要素へ変換することを責務に持つ """

    def is_target(self, blocks: list[Block]) -> bool:
        """
        参照しているBlock要素が目次要素であるか判定

        :param blocks: 参照しているBlock要素
        :return: Block要素が目次と対応->True, それ以外->False
        """
        # converterは同種のBlock単位で処理するので、もし目次のBlockが処理対象であった場合、単独で存在する
        toc_candidate = blocks[0]
        return isinstance(toc_candidate, TableOfContentsBlock)

    def convert(self, markdown_result: ParseResult) -> list[ListBlock]:
        """
        ヘッダから目次を表現するul liの木を構築

        :param markdown_result: ヘッダを含むBlock要素のリスト
        :return: 目次を表現するul li Blockのリスト
        """

        # 目次の構成要素として必要なヘッダのみ抽出
        header_list = [block for block in markdown_result.content if isinstance(block, HeadingBlock)]

        # ヘッダ->TocNode->目次
        toc_node_list = TocNodeTreeGenerator().generate(header_list)
        return TocGenerator().generate(toc_node_list)
