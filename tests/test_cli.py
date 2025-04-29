import pytest

from eblint.linter import Linter, main
from pathlib import Path


def test_single_file(mocker):
    testfile = "tests/testfiles/linter/pass/default-checkers-pass.eb"
    mocker.patch("sys.argv", ["eblint", testfile])
    mocker.patch("eblint.linter.Linter.run")
    main()
    Linter.run.assert_called_once_with(testfile)


def test_no_file(mocker):
    mocker.patch("eblint.linter.Linter.run")
    with pytest.raises(SystemExit):
        main()
    Linter.run.assert_not_called()


def test_wrong_file(mocker):
    non_existent_file = "tests/testfiles/non-existing-file.eb"
    assert not Path(non_existent_file).exists(), "Choose non-existing file"
    mocker.patch("sys.argv", ["eblint", non_existent_file])
    with pytest.raises(FileNotFoundError):
        main()


def test_multiple_files(mocker):
    file_1 = "tests/testfiles/linter/pass/default-checkers-pass.eb"
    file_2 = "tests/testfiles/linter/fail/M001/one-missing-field.eb"
    mocker.patch("sys.argv", ["eblint", file_1, file_2])
    mocker.patch("eblint.linter.Linter.run")
    main()
    Linter.run.assert_any_call(file_1)
    Linter.run.assert_called_with(file_2)
    assert Linter.run.call_count == 2, "Wrong number of calls"
