import argparse
import ast
from typing import Optional, Set, Union

from .checkers import DEFAULT_CHECKERS, Checker


class Linter:
    """A linter interface to run a file through multiple checkers.

    Attributes:
        checkers: collection of objects that check rules
    """

    def __init__(self, checkers: Optional[Union[Checker, Set[Checker]]] = None):
        """Initiate a linter.

        Args:
            checkers: the rule checkers to be attached to the linter
        """
        if checkers is None:
            self.checkers = set()
        elif isinstance(checkers, Checker):
            self.checkers = {checkers}
        else:
            self.checkers = checkers

    @staticmethod
    def print_violations(checker: Checker, filename: str):
        """Print all the violations found in a single file.

        Args:
            checker: checker whose violations to print
            filename: file in which the violations where found
        """
        for node, message in checker.violations:
            if isinstance(node, ast.expr):
                print(
                    f"{filename}:{node.lineno}:{node.col_offset}: "
                    f"{checker.issue_code}: {message}"
                )
            else:
                print(f"{filename}:1:0: {checker.issue_code}: {message}")

    def run(self, source_path: str, cleanup: bool = True):
        """Run a file through the linter.

        In between files it is important to reset the checkers to their original state.
        It is possible to omit this, but this might lead to unexpected behaviour.

        Args:
            source_path: path to the file to be checked
            cleanup: whether to reset the checkers to a clean state afterwards.
        """
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
    """Function for command line interface

    This function is invoked by the `eblint` command.
    """
    parser = argparse.ArgumentParser(
        prog="eblint", description="A linter for easybuild easyconfig files"
    )
    parser.add_argument("filename", nargs="+", help="File[s] to be linted")
    args = parser.parse_args()

    linter = Linter(checkers=DEFAULT_CHECKERS)

    for source_path in args.filename:
        linter.run(source_path)


if __name__ == "__main__":  # pragma: no cover
    main()
