import ast
import itertools
import os

import pytest

from eblint.checkers import FieldOrderChecker

order_filenames = {}

for strictness, pass_fail in itertools.product(["loose", "strict"], ["pass", "fail"]):
    folder = f"tests/testfiles/order_checker/{strictness}/{pass_fail}"
    with os.scandir(folder) as folder_iterator:
        case_filenames = [
            f"{folder}/{item.name}" for item in folder_iterator if item.is_file()
        ]
    nested_dict = order_filenames.setdefault(strictness, {})
    nested_dict.update({pass_fail: case_filenames})


@pytest.fixture
def order_checker() -> FieldOrderChecker:
    issue_code = "W345"
    field_names = [
        "ordered_field_1",
        "ordered_field_2",
        "ordered_field_3",
    ]
    return FieldOrderChecker(issue_code=issue_code, field_names=field_names)


@pytest.fixture
def strict_order_checker() -> FieldOrderChecker:
    issue_code = "W346"
    field_names = [
        "ordered_field_1",
        "ordered_field_2",
        "ordered_field_3",
    ]
    return FieldOrderChecker(
        issue_code=issue_code, field_names=field_names, strict_mode=True
    )


def test_attribute_values(order_checker):
    assert order_checker.issue_code == "W345"
    assert len(order_checker.violations) == 0
    assert order_checker.strict_mode is False


def test_strict_attribute_values(strict_order_checker):
    assert strict_order_checker.issue_code == "W346"
    assert len(strict_order_checker.violations) == 0
    assert strict_order_checker.strict_mode is True


@pytest.mark.parametrize("filename", order_filenames["loose"]["pass"])
def test_loose_passes(filename, order_checker):
    with open(filename) as file:
        tree = ast.parse(file.read())
    assert len(order_checker.violations) == 0
    order_checker.visit(tree)
    assert len(order_checker.violations) == 0


@pytest.mark.parametrize("filename", order_filenames["loose"]["fail"])
def test_loose_fails(filename, order_checker):
    with open(filename) as file:
        tree = ast.parse(file.read())
    assert len(order_checker.violations) == 0
    order_checker.visit(tree)
    assert len(order_checker.violations) > 0


@pytest.mark.parametrize("filename", order_filenames["strict"]["pass"])
def test_strict_passes(filename, strict_order_checker):
    with open(filename) as file:
        tree = ast.parse(file.read())
    assert len(strict_order_checker.violations) == 0
    strict_order_checker.visit(tree)
    assert len(strict_order_checker.violations) == 0


@pytest.mark.parametrize("filename", order_filenames["strict"]["fail"])
def test_strict_fails(filename, strict_order_checker):
    with open(filename) as file:
        tree = ast.parse(file.read())
    assert len(strict_order_checker.violations) == 0
    strict_order_checker.visit(tree)
    assert len(strict_order_checker.violations) > 0
