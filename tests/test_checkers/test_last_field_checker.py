import ast

import pytest

from eblint.checkers import LastFieldChecker


@pytest.fixture
def last_item_checker() -> LastFieldChecker:
    issue_code = "W234"
    last_field = "field_2"
    return LastFieldChecker(issue_code=issue_code, last_field_name=last_field)


def test_attribute_values(last_item_checker):
    assert last_item_checker.issue_code == "W234"
    assert len(last_item_checker.violations) == 0


def test_correct_format(last_item_checker):
    assert len(last_item_checker.violations) == 0
    test_tree = ast.parse("field_1 = 1; field_2 = 2")
    last_item_checker.visit(test_tree)
    assert len(last_item_checker.violations) == 0, "Ghost violations"


def test_field_not_last(last_item_checker):
    assert len(last_item_checker.violations) == 0
    test_tree = ast.parse("field_1 = 1; field_2 = 2; field_3 = 3")
    last_item_checker.visit(test_tree)
    assert len(last_item_checker.violations) == 1, "Violation missing"
    assert "field_2" in last_item_checker.violations.pop().message


def test_field_missing(last_item_checker):
    assert len(last_item_checker.violations) == 0
    test_tree = ast.parse("field_1 = 1; field_3 = 3")
    last_item_checker.visit(test_tree)
    assert len(last_item_checker.violations) == 1, "Violation missing"
    assert "field_2" in last_item_checker.violations.pop().message
