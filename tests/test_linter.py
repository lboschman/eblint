from eblint.linter import Linter


def test_empty_checkers():
    linter = Linter()
    assert isinstance(linter.checkers, set), "linter.checkers is not a set"
    assert len(linter.checkers) == 0, "linter.checkers is not empty"
