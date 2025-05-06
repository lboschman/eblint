import ast

import pytest

from eblint.checkers import ForbiddenFieldChecker, forbidden_field_checker


@pytest.fixture
def two_field_checker():
    checker = ForbiddenFieldChecker(
        issue_code="M005", forbidden_fields=["forbidden_field_1", "forbidden_field_2"]
    )
    yield checker
    checker.clear_violations()


def test_attributes(two_field_checker):
    assert two_field_checker.issue_code == "M005", "Wrong issue code"
    assert (
        len(two_field_checker.forbidden_fields) == 2
    ), "Wrong number of forbidden fields"
    assert (
        "forbidden_field_1" in two_field_checker.forbidden_fields
    ), "forbidden_field_1 not in checker.forbidden_fields"
    assert (
        "forbidden_field_2" in two_field_checker.forbidden_fields
    ), "forbidden_field_2 not in checker.forbidden_fields"
    assert len(two_field_checker.violations) == 0, "pre-existing violations"


def test_no_missing_fields(two_field_checker):
    test_tree = ast.parse("field_1 = 1; field_2 = 2")
    two_field_checker.visit(test_tree)
    assert len(two_field_checker.violations) == 0, "Ghost violations"


def test_one_missing_field(two_field_checker):
    test_tree = ast.parse("field_1 = 1; field_2 = 2; forbidden_field_1 = 3")
    two_field_checker.visit(test_tree)
    assert len(two_field_checker.violations) == 1, "Missing violation"
    assert "forbidden_field_1" in two_field_checker.violations.pop().message


def test_two_missing_fields(two_field_checker):
    test_tree = ast.parse(
        "field_1 = 1; field_2 = 2; forbidden_field_1 = 3; forbidden_field_2 = 4"
    )
    two_field_checker.visit(test_tree)
    assert len(two_field_checker.violations) == 2, "Missing violations"
    assert "forbidden_field_" in two_field_checker.violations.pop().message
    assert "forbidden_field_" in two_field_checker.violations.pop().message
