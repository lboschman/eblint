import ast

import pytest

from eblint.checkers import MandatoryFieldChecker


@pytest.fixture
def two_item_checker() -> MandatoryFieldChecker:
    issue_code = "W234"
    field_names = ["mandatory_field_1", "mandatory_field_2"]
    return MandatoryFieldChecker(issue_code=issue_code, field_names=field_names)


def test_default_values():
    issue_code = "W234"
    empty_list = []
    checker = MandatoryFieldChecker(issue_code=issue_code, field_names=empty_list)
    assert checker.issue_code == issue_code
    assert isinstance(
        checker.mandatory_field_names, list
    ), "Mandatory field names not a list"
    assert len(checker.mandatory_field_names) == 0, "mandatory_field_names not empty"


def test_two_item_list(two_item_checker):
    assert len(two_item_checker.mandatory_field_names) == 2
    assert "mandatory_field_1" in two_item_checker.mandatory_field_names
    assert "mandatory_field_2" in two_item_checker.mandatory_field_names


def test_missing_item(two_item_checker):
    assert len(two_item_checker.violations) == 0
    test_tree = ast.parse("mandatory_field_1 = 1")
    two_item_checker.visit(test_tree)
    assert len(two_item_checker.violations) == 1, "Violation missing"
    assert "mandatory_field_2" in two_item_checker.violations.pop().message


def test_no_missing_item(two_item_checker):
    assert len(two_item_checker.violations) == 0
    test_tree = ast.parse("mandatory_field_1 = 1; mandatory_field_2 = 2")
    two_item_checker.visit(test_tree)
    assert len(two_item_checker.violations) == 0, "Ghost violations"
