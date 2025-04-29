import argparse
import ast
from typing import Set, Union

from .checkers import DEFAULT_CHECKERS, Checker


class Linter:
    def __init__(self, checkers: Union[Checker, Set[Checker]] = set()):
        self.checkers = checkers if not isinstance(checkers, Checker) else {checkers}

    @staticmethod
    def print_violations(checker: Checker, filename: str):
        for node, message in checker.violations:
            if isinstance(node, ast.expr):
                print(
                    f"{filename}:{node.lineno}:{node.col_offset}: "
                    f"{checker.issue_code}: {message}"
                )
            else:
                print(f"{filename}:1:0: {checker.issue_code}: {message}")

    def run(self, source_path, cleanup: bool = True):
        with open(source_path, "r") as source_file:
            source_code = source_file.read()

        tree = ast.parse(source_code)
        for checker in self.checkers:
            checker.visit(tree)
            self.print_violations(checker, source_path)

        if cleanup is True:
            self.clear_violations()

    def clear_violations(self):
        for checker in self.checkers:
            checker.clear_violations()


def main():
    parser = argparse.ArgumentParser(
        prog="eblint", description="A linter for easybuild easyconfig files"
    )
    parser.add_argument("filename", nargs="+", help="File[s] to be linted")
    args = parser.parse_args()

    linter = Linter(checkers=DEFAULT_CHECKERS)

    for source_path in args.filename:
        linter.run(source_path)


if __name__ == "__main__":
    main()
