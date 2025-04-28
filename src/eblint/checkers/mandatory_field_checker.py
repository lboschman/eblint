import ast

from . import Checker, Violation


class MandatoryFieldChecker(Checker):
    """Checks the presence of mandatory fields."""

    def __init__(self, issue_code, field_names):
        super().__init__(issue_code)
        self.mandatory_field_names = field_names
        self.seen_field_names = []

    def visit_Name(self, node: ast.Name):
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
