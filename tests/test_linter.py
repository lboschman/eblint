import os
from typing import List, Tuple

import pytest

from eblint.checkers import DEFAULT_CHECKERS, MandatoryFieldChecker
from eblint.linter import Linter

DEFAULT_ISSUE_CODES = [c.issue_code for c in DEFAULT_CHECKERS]

fail_filenames: List[Tuple] = []
for issue_code in DEFAULT_ISSUE_CODES:
    folder = f"tests/testfiles/linter/fail/{issue_code}"
    with os.scandir(folder) as folder_iterator:
        filenames = [
            f"{folder}/{item.name}" for item in folder_iterator if item.is_file()
        ]
    for fname in filenames:
        fail_filenames.append((issue_code, fname))

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


@pytest.mark.parametrize("issue_code,filename", fail_filenames)
def test_default_linter_fail(issue_code, filename, default_linter):
    default_linter.clear_violations()
    for checker in default_linter.checkers:
        assert len(checker.violations) == 0, "Violations not cleared"
    default_linter.run(filename, cleanup=False)
    for checker in default_linter.checkers:
        if checker.issue_code == issue_code:
            assert (
                len(checker.violations) > 0
            ), f"Passed {checker.issue_code} on bad file {filename}"
        else:
            assert (
                len(checker.violations) == 0
            ), f"Failed {checker.issue_code} on good file {filename}"
