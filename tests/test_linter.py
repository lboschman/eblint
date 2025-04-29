import pytest

from eblint.checkers import MandatoryFieldChecker
from eblint.linter import Linter


@pytest.fixture
def mandatory_field_linter():
    checker = MandatoryFieldChecker(issue_code="M001", field_names=["mandatory_field"])
    linter = Linter(checker)
    return linter


def test_empty_checkers():
    linter = Linter()
    assert isinstance(linter.checkers, set), "linter.checkers is not a set"
    assert len(linter.checkers) == 0, "linter.checkers is not empty"


def test_default_linter(mandatory_field_linter):
    assert isinstance(
        mandatory_field_linter.checkers, set
    ), "linter.checkers is not a set"
    assert len(mandatory_field_linter.checkers) == 1, "linter.checkers is empty"
