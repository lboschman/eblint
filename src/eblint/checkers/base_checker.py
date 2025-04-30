import ast
from typing import Set

from .violation import Violation


class Checker(ast.NodeVisitor):
    """Checks a body of text for violations.

    Attributes:
        issue_code: unique identifier for this type of violations
        violations: set of violations collected
    """
    def __init__(self, issue_code: str):
        """Initiate Checker.

        Args:
            issue_code: unique identifier for this type of violations
        """
        self.issue_code = issue_code
        self.violations: Set[Violation] = set()

    def clear_violations(self):
        """Reset violations to an empty set."""
        self.violations = set()
