import ast
from typing import List

from .base_checker import Checker
from .violation import Violation


class MandatoryFieldChecker(Checker):
    """Checks the presence of mandatory fields.

    Attributes:
        mandatory_field_names: field names that should be present
        seen_field_names: fields encountered in a file, for housekeeping
    """

    def __init__(self, issue_code: str, field_names: List[str]):
        """Create MandatoryFieldChecker.

        Args:
            issue_code: Code for these particular fields
            field_names: list of mandatory fields
        """
        super().__init__(issue_code)
        self.mandatory_field_names = field_names
        self.seen_field_names = []

    def visit_Name(self, node: ast.Name):
        """Visit Name node.

        Args:
            node: node to be visited.
        """
        if isinstance(node.ctx, ast.Store):
            self.seen_field_names.append(node.id)
        super().generic_visit(node)

    def visit_Module(self, node: ast.Module):
        """Visit a module.

        Missing mandatory fields are checked after visiting the entire module.
        Afterwards, the checker is reset to its original state.

        Args:
            node: module to be visited
        """
        super().generic_visit(node)
        for name in self.mandatory_field_names:
            if name not in self.seen_field_names:
                self.violations.add(
                    Violation(node, f"Missing mandatory field '{name}'")
                )
        self.seen_field_names = []
