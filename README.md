# 概要

ブログの記事をいい感じに表示するために、Pythonでマークダウンパーサをつくりました。

## サンプル

HTMLの各タグにはCSSのクラス名を指定することができ、デフォルトではtailwindcssで下図のようなスタイルが適用されます。

![image](https://user-images.githubusercontent.com/43694794/147841114-4ee9f74b-c2fa-40ff-9f04-9223b7c93b90.png)

## usage

```bash
# install pipenv
pipenv install git+https://github.com/a-pompom/Python-markdownParser.git#egg=a_pompom_markdown_parser

# parse-cli
a_pompom_markdown_parser <in_file_path> <out_file_path>
# parse-string
a_pompom_markdown_parser <markdown_string>
```