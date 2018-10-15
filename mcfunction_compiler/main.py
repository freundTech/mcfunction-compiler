import sys

from lark import Lark
from argparse import ArgumentParser
from pkg_resources import resource_string
from pathlib import Path

from codegeneration import CodeGenerator
from transformer import TreeTransformer
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

    grammar = resource_string("mcfunction_compiler.resources", "grammar.lark").decode()
    l = Lark(grammar, parser="earley")

    with input_path.open() as file:
        tree = l.parse(file.read())

        t = TreeTransformer()
        ast = t.transform(tree)
        ast.accept(NameResolver())
        generator = CodeGenerator()
        ast.accept(generator)
        generator.write_to_files(output_path)

