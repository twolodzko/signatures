import argparse
import glob
import token
from tokenize import tokenize


def parse_args():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [pattern]",
        description="Find signatures of all the functions and methods in the source code.",
    )
    parser.add_argument(
        "pattern",
        help="pattern to identify files to be analyzed",
        type=str,
        nargs="?",
        default="**/*.py",
    )
    return parser.parse_args()


def find_definitions(filename):
    # This code comes from:
    # https://stackoverflow.com/questions/38180661/how-to-print-signatures-of-all-functions-methods-in-a-python-project

    with open(filename, "rb") as f:
        gen = tokenize(f.readline)
        for tok in gen:
            if tok.type == token.NAME and tok.string == "def":
                # function definition, read until next colon outside
                # parentheses.
                definition, last_line = [tok.line], tok.end[0]
                parens = 0
                while tok.exact_type != token.COLON or parens > 0:
                    if last_line != tok.end[0]:
                        definition.append(tok.line)
                        last_line = tok.end[0]
                    if tok.exact_type == token.LPAR:
                        parens += 1
                    elif tok.exact_type == token.RPAR:
                        parens -= 1
                    tok = next(gen)
                if last_line != tok.end[0]:
                    definition.append(tok.line)
                yield "".join(definition)


def cli():
    args = parse_args()
    for file in glob.glob(args.pattern, recursive=True):
        print(file)
        for definition in find_definitions(filename=file):
            print(f"  {definition.rstrip()}")
        print()


if __name__ == "__main__":
    cli()
