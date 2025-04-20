import ast
import os
import sys
import re
from typing import NamedTuple, Set


class Violation(NamedTuple):
    node: ast.AST
    message: str


class Checker(ast.NodeVisitor):
    def __init__(self, issue_code):
        self.issue_code = issue_code
        self.violations: Set[Violation] = set()


class Linter:
    def __init__(self):
        self.checkers: Set[Checker] = set()

    @staticmethod
    def print_violations(checker: Checker, filename: str):
        for node, message in checker.violations:
            try:
                print(
                    f"{filename}:{node.lineno}:{node.col_offset}: "
                    f"{checker.issue_code}: {message}"
                )
            except AttributeError:
                print(f"{filename}: {checker.issue_code}: {message}")

    def run(self, source_path):
        filename = os.path.basename(source_path)

        with open(source_path, "r") as source_file:
            source_code = source_file.read()

        tree = ast.parse(source_code)
        for checker in self.checkers:
            checker.visit(tree)
            self.print_violations(checker, filename)


class MandatoryFieldChecker(Checker):
    def __init__(self, issue_code, field_names):
        super().__init__(issue_code)
        self.mandatory_field_names = field_names
        self.seen_field_names = []

    def visit_Name(self, node: ast.AST):
        # for target in node.targets:
        if isinstance(node.ctx, ast.Store):
            self.seen_field_names.append(node.id)
        super().generic_visit(node)

    def visit_Module(self, node):
        super().generic_visit(node)
        for name in self.mandatory_field_names:
            if name not in self.seen_field_names:
                self.violations.add(
                    Violation(node, f"Missing mandatory field '{name}'")
                )


def main():
    source_path = sys.argv[1]

    linter = Linter()
    linter.checkers.add(
        MandatoryFieldChecker(
            issue_code="M001", field_names=["easyblock", "name", "versionnumber"]
        )
    )

    linter.run(source_path)


if __name__ == "__main__":
    main()
