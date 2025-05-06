import ast
from typing import List

from .base_checker import Checker
from .violation import Violation


class ForbiddenFieldChecker(Checker):
    """Checker for fields that should not be mentioned in public EasyConfig files.

    Attributes:
        forbidden_fields: list of forbidden fields
    """
    def __init__(self, issue_code: str, forbidden_fields: List[str]):
        """Initiate ForbiddenFieldChecker.

        Args:
            issue_code: the issue code the linter associates with these forbidden fields
            forbidden_fields: list of forbidden fields
        """
        super().__init__(issue_code)
        self.forbidden_fields = forbidden_fields

    def visit_Name(self, node: ast.Name):
        """Visit a Name node.

        Args:
            node: node to be visited
        """
        if node.id in self.forbidden_fields:
            self.violations.add(
                Violation(
                    node=node,
                    message=f"{node.id} should not be defined in EB config file",
                )
            )
        super().generic_visit(node)
