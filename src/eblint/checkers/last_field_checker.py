import ast
from typing import Optional

from .base_checker import Checker
from .violation import Violation


class LastFieldChecker(Checker):
    """Checker to ensure the last field in an eb-config file is a particular field.

    Attributes:
        last_field_name: name of the field that should be last
        last_visited_field_node: node that was visited last, for housekeeping
    """

    def __init__(self, issue_code: str, last_field_name: str = "moduleclass"):
        """Create LastFieldChecker.

        Args:
            issue_code: code associated with this rule
            last_field_name: field that should be last
        """
        super().__init__(issue_code)
        self.last_field_name = last_field_name
        self.last_visited_field_node: Optional[ast.Name] = None

    def visit_Name(self, node: ast.Name):
        """Visit a Name node.

        Args:
            node: node to be visited
        """
        self.last_visited_field_node = node
        super().generic_visit(node)

    def visit_Module(self, node: ast.Module):
        """Visit and leave a module.

        It is impossible to see if the rule has been met until the module has been
        completely read.
        Afterwards, the checker is reset to its original state.

        Args:
            node: module to be visited.
        """
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
        self.last_visited_field_node = None
