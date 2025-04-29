import ast
from typing import NamedTuple


class Violation(NamedTuple):
    """A violation of a rule.

    Attributes:
        node: the node where the violation happened
        message: message to display
    """
    node: ast.AST
    message: str
