# 変換するときの改行コード・インデント・クラス名などの設定値
setting = {
    'newline_code': '\n',
    'indent': '    ',

    # スタイルのクラス名
    'class_name': {
        'h1': 'mt-8 mb-8 text-4xl font-sans font-bold border-solid border-indigo-400 border-b-2 pb-1.5',
        'h2': 'pb-1 mt-4 mb-4 font-sans text-2xl font-semibold border-b-2 border-indigo-400 border-solid',
        'h3': 'mt-4 mb-4 font-sans text-xl font-semibold',
        'h4': 'mt-4 mb-4 text-lg',
        'p': 'mt-2 mb-2',

        'ul': 'mt-4 ml-8 list-disc',
        'li': 'mt-2',
        'blockquote': 'pl-4 border-l-2 border-gray-400 border-solid text-slate-400',
        'hr': 'border-b-2 border-indigo-400',

        'code': 'bg-slate-700',
        'a': 'text-sky-300',
    },
    'class_name_with_template': {
        'code_block': 'language-{language} hljs'
    }
}
