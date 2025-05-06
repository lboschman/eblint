import ast
from typing import List

from .base_checker import Checker
from .violation import Violation


class ForbiddenFieldChecker(Checker):
    def __init__(self, issue_code: str, forbidden_fields: List[str]):
        super().__init__(issue_code)
        self.forbidden_fields = forbidden_fields

    def visit_Name(self, node: ast.Name):
        if node.id in self.forbidden_fields:
            self.violations.add(
                Violation(
                    node=node,
                    message=f"{node.id} should not be defined in EB config file",
                )
            )
