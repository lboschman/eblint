from eblint.checkers import Checker


def test_default_checker_properties():
    issue_code = "W123"
    checker = Checker(issue_code)
    assert checker.issue_code == issue_code, "Issuecode stored incorrectly in checker"
    assert isinstance(checker.violations, set)
    assert len(checker.violations) == 0, "checker.violations not empty"
