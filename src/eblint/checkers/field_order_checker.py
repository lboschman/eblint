import ast
from typing import List

from .base_checker import Checker
from .violation import Violation


class FieldOrderChecker(Checker):
    """Checks the order of the fields in an eb-config file.

    In regular mode, the FieldOrderChecker only checks if the listed fields are in
    the defined order. Defined fields that are missing and undefined fields do not
    raise an error.

    In strict mode, all the defined fields should appear before the undefined fields.
    Missing defined fields do not raise an error.
    Mandatory fields should be checked with the MandatoryFieldChecker.

    UnOrderedField1 = ... <-- raises error in strict mode
    OrderedField1 = ...
    UnOrderedField2 = ... <-- raises error in strict mode
    OrderedField2 = ...
    UnOrderedField3 = ... <-- raises error in strict mode
    OrderedField4 = ...
    UnOrderedField4 = ... <-- raises error in strict mode
    OrderedField3 = ... <-- raises error

    """

    def __init__(
        self, issue_code: str, field_names: List[str], strict_mode: bool = False
    ):
        """Initiate FieldOrderChecker.

        Args:
            issue_code: code associated with this particular ordering
            field_names: field names that should be in that order
            strict_mode: whether the ordering should be enforced in strict mode
        """
        super().__init__(issue_code)
        self.ordered_fieldnames = field_names
        self.seen_ordered_fields = []
        self.seen_ordered_fields_indices = [
            -1,
        ]
        self.strict_mode = strict_mode

    def visit_Name(self, node: ast.Name):
        """Visit a Name node

        Args:
            node: the node to be visited
        """
        if (
            node.id in self.ordered_fieldnames or self.strict_mode is True
        ) and isinstance(node.ctx, ast.Store):
            try:
                seen_field_index = self.ordered_fieldnames.index(node.id)
            except ValueError:
                seen_field_index = 9001
            if seen_field_index < self.seen_ordered_fields_indices[-1]:
                if self.strict_mode is True:
                    wrong_ordered_field = self.seen_ordered_fields[-1]
                else:
                    wrong_ordered_field = [
                        field
                        for field in self.seen_ordered_fields
                        if field in self.ordered_fieldnames
                    ][-1]
                self.violations.add(
                    Violation(
                        node,
                        f"'{wrong_ordered_field}' defined before '{node.id}'",
                    )
                )

            self.seen_ordered_fields_indices.append(seen_field_index)
            self.seen_ordered_fields.append(node.id)

        super().generic_visit(node)

    def visit_Module(self, node: ast.Module):
        """Inspect a full module.

        After visiting, the checker is reset to its original state.

        Args:
            node: the file to be visited
        """
        super().generic_visit(node)
        self.seen_ordered_fields = []
        self.seen_ordered_fields_indices = [
            -1,
        ]
