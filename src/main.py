import sys

from lark import Lark
from argparse import ArgumentParser
from pkg_resources import resource_string
from pathlib import Path

from transformer import TreeTransformer, token_to_boolean, token_to_int, token_to_string
from visitor import NameResolver

if __name__ == "__main__":
    parser = ArgumentParser(description="Compile .mccode files to .mcfunction")
    parser.add_argument("input", metavar="INPUT", type=str, help=".mccode file to compile")
    parser.add_argument("-o", "--output", action="store", default="out", help="directory to store the datapack in")

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists() or input_path.is_dir():
        print(f"No such file: '{input_path}'", file=sys.stderr)
        exit(1)

    output_path = Path(args.output)
    if not output_path.exists():
        output_path.mkdir()
    if not output_path.is_dir():
        print(f"'{output_path}' is not a directory", file=sys.stderr)
        exit(1)

    grammar = resource_string(__name__, "grammar.lark").decode()
    l = Lark(grammar, parser="earley", lexer_callbacks={
        'INT': token_to_int,
        'BOOLEAN': token_to_boolean,
        'STRING': token_to_string,
    })

    with input_path.open() as file:
        tree = l.parse(file.read())

        print(tree)
        print(tree.pretty())
        t = TreeTransformer()
        ast = t.transform(tree)
        ast.accept(NameResolver())
