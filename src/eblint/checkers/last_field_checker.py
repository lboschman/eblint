import ast
from typing import Optional

from . import Checker, Violation


class LastFieldChecker(Checker):
    """Checks that the last field in an eb-config file is a particuler field."""

    def __init__(self, issue_code: str, last_field_name: str = "moduleclass"):
        super().__init__(issue_code)
        self.last_field_name = last_field_name
        self.last_visited_field_node: Optional[ast.Name] = None

    def visit_Name(self, node: ast.Name):
        self.last_visited_field_node = node
        super().generic_visit(node)

    def visit_Module(self, node: ast.Module):
        super().generic_visit(node)
        if (
            self.last_visited_field_node is not None
            and self.last_visited_field_node.id != self.last_field_name
        ):
            self.violations.add(
                Violation(
                    self.last_visited_field_node,
                    f"Last defined field must be '{self.last_field_name}'",
                )
            )
