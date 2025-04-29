import os

import pytest

from eblint.checkers import MandatoryFieldChecker
from eblint.linter import Linter

pass_folder = "tests/testfiles/linter/pass"
with os.scandir(pass_folder) as folder_iterator:
    pass_filenames = [
        f"{pass_folder}/{item.name}" for item in folder_iterator if item.is_file()
    ]


@pytest.fixture
def mandatory_field_linter():
    checker = MandatoryFieldChecker(issue_code="M001", field_names=["mandatory_field"])
    linter = Linter(checker)
    return linter


@pytest.fixture
def default_linter():
    return Linter(DEFAULT_CHECKERS)


def test_empty_checkers():
    linter = Linter()
    assert isinstance(linter.checkers, set), "linter.checkers is not a set"
    assert len(linter.checkers) == 0, "linter.checkers is not empty"


def test_small_linter(mandatory_field_linter):
    assert isinstance(
        mandatory_field_linter.checkers, set
    ), "linter.checkers is not a set"
    assert len(mandatory_field_linter.checkers) == 1, "linter.checkers is empty"


@pytest.mark.parametrize("filename", pass_filenames)
def test_default_linter_pass(filename, default_linter):
    for checker in default_linter.checkers:
        assert len(checker.violations) == 0
    default_linter.run(filename)
    for checker in default_linter.checkers:
        assert len(checker.violations) == 0, f"Failed {checker.issue_code} on good file"
