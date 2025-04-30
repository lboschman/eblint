import ast
import re
from typing import List

from .base_checker import Checker
from .violation import Violation


class DependencyFormatChecker(Checker):
    """Checker for dependency format

    Attributes:
        VERSION_FORMAT: format for version code
        PACKAGE_NAME_FORMAT: format for package name
        dependency_keywords: which fields contain a list of dependencies
        stored_names: variable definitions for later evaluation
    """
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
            if target.id in self.dependency_keywords and isinstance(
                target.ctx, ast.Store
            ):
                self.check_dependency_list(node.value)
            else:
                self.stored_names.update({target.id: node.value})
        super().generic_visit(node)
