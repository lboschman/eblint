import ast
from typing import NamedTuple

class Violation(NamedTuple):
    node: ast.AST
    message: str
