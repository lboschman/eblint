import ast
import sys
from typing import Set

from .checkers import DEFAULT_CHECKERS, Checker


class Linter:
    def __init__(self, checkers: Set[Checker] = set()):
        self.checkers = checkers

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

    def run(self, source_path):
        with open(source_path, "r") as source_file:
            source_code = source_file.read()

        tree = ast.parse(source_code)
        for checker in self.checkers:
            checker.visit(tree)
            self.print_violations(checker, source_path)


def main():
    source_path = sys.argv[1]

    linter = Linter(checkers=DEFAULT_CHECKERS)

    linter.run(source_path)


if __name__ == "__main__":
    main()
