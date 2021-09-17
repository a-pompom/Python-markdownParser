# アーキテクチャ設計

本文書では、各アーキテクチャの概要、およびなぜそのアーキテクチャに至ったか、経緯を記す。

## フロー概略


```{mermaid}
sequenceDiagram
    participant App
    participant Parser
    participant Converter
    participant Generator
    participant HTMLFile
    App ->> Parser: マークダウンファイルを渡す
    Parser ->> Converter: マークダウン変換結果を受け取り
    Converter ->> Generator: HTML入力を渡す
    Generator ->> HTMLFile: 変換結果HTMLを出力
```

```{mermaid}
stateDiagram-v2
    [*] --> App
    App --> MarkdownParser
  
    state MarkdownParser {
        [*] --> Parser
        Parser --> HeadingParser
        Parser --> ListParser
    }
    
    MarkdownParser --> Converter
    Converter --> HTMLGenerator
    
    state HTMLGenerator {
        [*] --> Generator
        Generator --> HeadingGenerator
        Generator --> ListGenerator
    }
```

## マークダウンパーサ

マークダウンの解析を責務に持つ。
ファイルを1行ずつ解釈し、マークダウン変換結果オブジェクトを生成。

マークダウンパーサは、HTMLを知ることなく、マークダウンだけで完結させたいので、
HTMLとの対応付けは中継処理へ委譲。
本処理は、マークダウンの記法の種類が何であるかを解析するに留める。

このようにオブジェクトが知る範囲を最小限にすることで、設計・テストの負荷を下げることができる。

### マークダウン変換結果オブジェクト

マークダウンの各行・要素単位で変換結果を格納。

本オブジェクトは、`Block`と`Inline`の2つの要素から構成されている。
Blockでは、ヘッダやリストなど、行単位のスタイルの種類を保持。
一方、Inlineでは、クォートや強調など、インラインでのスタイルの種類を保持。

#### データ構造

より具体的な形をイメージするため、BlockとInlineそれぞれのデータ構造を簡単に記述する。

Blockは、マークダウン変換結果オブジェクト上にリスト形式で保持される。
それぞれがプロパティ上にヘッダやリストなど、スタイルの種類を持つ。
更に、各要素は`children`をプロパティとして持ち、テキストやInline・ネストしたブロックを格納。

Inlineは、Blockのchildrenプロパティ上で保持される。
インライン上のテキストやスタイルをプロパティとして持ち、`*strong*`のようなインラインスタイルを表現。

---

#### 補足: なぜBlockとInlineで分けたのか

マークダウンの解析処理は、行を単位としている。
ヘッダやリストといった、行単位のスタイルが重複することはない。例えば、ヘッダの中でリストを書くようなことはできない。

しかし、Inlineは行の中でいくつでも書くことができるので、Blockとは扱いが異なる。
Blockは、「行にどのようなスタイルを適用するか」・Inlineは、「要素にどのようなスタイルを適用するか」を意味しているので、
互いに独立している。
独立した要素は分離した方がシンプルに扱えるので、それぞれを別々に分けることにした。


### 中継処理

マークダウンの変換結果を受け取り、HTML生成処理の入力用オブジェクトを生成することを責務に持つ。

中継する役割のクラスを挟むことで、マークダウン/HTMLを処理するクラスはお互いのことを知る必要がなくなる。

#### HTML入力オブジェクトの生成

基本的には単なるマッピングだが、HTMLでは、リスト(ul, li)のようにネストした構造をとることがある。
先ほどのBlock・Inlineをベースに、構造を拡張することでこれを実現する。

リストを具体例に考えてみる。マークダウンでは`* から始まる行であるリストのスタイル`という情報のみ保持していたが、
HTMLでは、ul・liそれぞれを表すものが必要である。
ulを表すBlock, liを表すBlock, ulの終端を表すBlockといったように、よりHTMLへ近い形へ
変換結果オブジェクトを変換する。HTMLと対応する形へ解釈できれば、HTMLを生成するオブジェクトは、
入力をそのままHTMLのツリーへマッピングできるようになる。

---

Blockは子にBlockまたはInlineを持つようになる。 これは、HTMLタグの階層構造に近い。
このような構造をとることで、リストや引用文のような、連続して続くような記法にも対応できる。


### HTML組み立て処理

HTML入力オブジェクトを受け取り、HTML文字列を生成。
入力である変換結果オブジェクトが持つ階層構造を順に解釈していくことで、HTMLを文字列としてつくり出すことができる。

あとは、変換結果を呼び出し元へ返却すれば、マークダウンからHTMLへ変換された文字列が手に入る。