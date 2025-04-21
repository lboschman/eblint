import ast
import os
import re
import sys
from ast import Store
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
    """Checks the presence of mandatory fields."""

    def __init__(self, issue_code, field_names):
        super().__init__(issue_code)
        self.mandatory_field_names = field_names
        self.seen_field_names = []

    def visit_Name(self, node: ast.AST):
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
    """Checks the order of the fields in an eb-config file.

    In regular mode, the FieldOrderChecker only checks if the listed fields are in
    the defined order. Defined fields that are missing and undefined fields do not
    raise an error.

    In strict mode, all the defined fields should appear before the undefined fields.
    Missing defined fields do not raise an error.
    Mandatory fields should be checked with the MandatoryFieldChecker.

    UnOrderedField1 = ... <-- raises error in strict mode
    OrderedField1 = ...
    UnOrderedField2 = ... <-- raises error in strict mode
    OrderedField2 = ...
    UnOrderedField3 = ... <-- raises error in strict mode
    OrderedField4 = ...
    UnOrderedField4 = ... <-- raises error in strict mode
    OrderedField3 = ... <-- raises error

    """

    def __init__(self, issue_code, field_names: List[str], strict_mode: bool = False):
        super().__init__(issue_code)
        self.ordered_fieldnames = field_names
        self.seen_ordered_fields = []
        self.seen_ordered_fields_indices = [
            -1,
        ]
        self.strict_mode = strict_mode

    def visit_Name(self, node):
        if (
            node.id in self.ordered_fieldnames or self.strict_mode is True
        ) and isinstance(node.ctx, ast.Store):
            try:
                seen_field_index = self.ordered_fieldnames.index(node.id)
            except ValueError:
                seen_field_index = 9001
            if seen_field_index < self.seen_ordered_fields_indices[-1]:
                if self.strict_mode is True:
                    wrong_ordered_field = self.seen_ordered_fields[-1]
                else:
                    wrong_ordered_field = [
                        field
                        for field in self.seen_ordered_fields
                        if field in self.ordered_fieldnames
                    ][-1]
                self.violations.add(
                    Violation(
                        node,
                        f"'{wrong_ordered_field}' defined before '{node.id}'",
                    )
                )

            self.seen_ordered_fields_indices.append(seen_field_index)
            self.seen_ordered_fields.append(node.id)

        super().generic_visit(node)


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
                    f"Incorrectly formatted package name/version: {value_string}",
                )
            )

    def check_dependency_list(self, node):
        for child in node.elts:
            self.check_dependency_tuple(child)

    def check_dependency_tuple(self, node):
        self.check_string_format(node.elts[0], self.PACKAGE_NAME_FORMAT)
        self.check_string_format(node.elts[1], self.VERSION_FORMAT)

    def visit_Assign(self, node):
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
            issue_code="M001", field_names=["easyblock", "name", "versionnumber"]
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
            field_names=["easyblock", "name", "versionsuffixer"],
            strict_mode=True,
        )
    )

    linter.checkers.add(
        DependencyFormatChecker("D001"),
    )

    linter.run(source_path)


if __name__ == "__main__":
    main()
