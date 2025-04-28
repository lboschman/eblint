import ast
from typing import Set

class Checker(ast.NodeVisitor):
    def __init__(self, issue_code: str):
        self.issue_code = issue_code
        self.violations: Set[Violation] = set()
