import setuptools

setuptools.setup(
    name="a_pompom_markdown_parser",
    version="1.1.7",
    author="a-pompom",
    author_email="",
    description="",
    url="https://github.com/a-pompom/Python-markdownParser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['a_pompom_markdown_parse = a_pompom_markdown_parser.main:execute']
    },
    python_requires='>=3.10',
)
