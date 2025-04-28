import ast
import re
import sys
from ast import Store
from typing import List, Set

from .checkers import Checker, MandatoryFieldChecker, FieldOrderChecker


class Linter:
    def __init__(self):
        self.checkers: Set[Checker] = set()

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


class DependencyFormatChecker(Checker):
    VERSION_FORMAT = r"\d+((\.\d+)*)"
    PACKAGE_NAME_FORMAT = r"\w*"

    def __init__(
        self,
        issue_code,
        dependency_keywords: List[str] = ["dependencies", "builddependencies"],
    ):
        super().__init__(issue_code)
        self.dependency_keywords = dependency_keywords
        self.stored_names = {}

    def check_string_format(self, string_node, format):
        if isinstance(string_node, ast.Name):
            value_string = self.stored_names[string_node.id].value
        else:
            value_string = string_node.value

        if re.fullmatch(format, value_string) is None:
            self.violations.add(
                Violation(
                    string_node,
                    f"Incorrectly formatted package name/version: '{value_string}'",
                )
            )

    def check_dependency_list(self, node):
        for child in node.elts:
            self.check_dependency_tuple(child)

    def check_dependency_tuple(self, node):
        self.check_string_format(node.elts[0], self.PACKAGE_NAME_FORMAT)
        self.check_string_format(node.elts[1], self.VERSION_FORMAT)

    def visit_Assign(self, node: ast.Assign):
        for target in node.targets:
            if target.id in self.dependency_keywords and isinstance(target.ctx, Store):
                self.check_dependency_list(node.value)
            else:
                self.stored_names.update({target.id: node.value})
        super().generic_visit(node)


def main():
    source_path = sys.argv[1]

    linter = Linter()
    linter.checkers.add(
        MandatoryFieldChecker(
            issue_code="M001",
            field_names=[
                "easyblock",
                "name",
                "version",
                "versionsuffixer",
                "dependencies",
                "builddependencies",
                "toolchain",
            ],
        )
    )
    linter.checkers.add(
        FieldOrderChecker(
            "M002",
            field_names=["easyblock", "name", "version", "versionsuffixer"],
        )
    )
    linter.checkers.add(
        FieldOrderChecker(
            "M003",
            field_names=["easyblock", "name", "version", "versionsuffixer"],
            strict_mode=True,
        )
    )

    linter.checkers.add(
        DependencyFormatChecker(
            "D001", dependency_keywords=["dependencies", "builddependencies"]
        ),
    )

    linter.run(source_path)


if __name__ == "__main__":
    main()
