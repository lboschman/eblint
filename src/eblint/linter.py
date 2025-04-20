import ast
import os
import re
import sys
from typing import List, NamedTuple, Set


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


class FieldOrderChecker(Checker):
    def __init__(self, issue_code, field_names: List[str]):
        super().__init__(issue_code)
        self.ordered_fieldnames = field_names
        self.seen_ordered_fields = []
        self.seen_ordered_fields_indices = [
            -1,
        ]

    def visit_Name(self, node):
        if node.id in self.ordered_fieldnames:
            seen_field_index = self.ordered_fieldnames.index(node.id)
            if seen_field_index < self.seen_ordered_fields_indices[-1]:
                self.violations.add(
                    Violation(
                        node,
                        f"Field {node.id} defined after {self.seen_ordered_fields[-1]}",
                    )
                )

            self.seen_ordered_fields_indices.append(seen_field_index)
            self.seen_ordered_fields.append(node.id)

        super().generic_visit(node)


def main():
    source_path = sys.argv[1]

    linter = Linter()
    linter.checkers.add(
        MandatoryFieldChecker(
            issue_code="M001", field_names=["easyblock", "name", "versionnumber"]
        )
    )
    linter.checkers.add(
        FieldOrderChecker(
            "M002", field_names=["easyblock", "name", "version", "versionsuffixer"]
        )
    )

    linter.run(source_path)


if __name__ == "__main__":
    main()
