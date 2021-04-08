"""Tests for 'files' argument of hunspellcheck CLI utilities."""

import argparse
import contextlib
import io
import os
import shutil
import tempfile

import pytest

from hunspellcheck.cli import extend_argument_parser


@pytest.mark.parametrize("files", (True, False))
def test_extend_argument_parser__files(files):
    parser = argparse.ArgumentParser()
    extend_argument_parser(
        parser,
        files=files,
        languages=False,
        personal_dict=False,
    )

    tempdir = tempfile.gettempdir()
    filenames = [
        os.path.join(tempdir, "hunspellcheck-foo.txt"),
        os.path.join(tempdir, "hunspellcheck-bar.txt"),
    ]

    for filename in filenames:
        with open(filename, "w") as f:
            f.write("")

    if files:
        opts = parser.parse_args([filenames[0]])
        assert len(opts.files) == 1
        assert opts.files[0] == filenames[0]

        # multiple files
        opts = parser.parse_args(filenames)
        assert len(opts.files) == 2
        assert opts.files[0] == filenames[0]
        assert opts.files[1] == filenames[1]
    else:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), pytest.raises(SystemExit):
            parser.parse_args(filenames)

        filenames_string = " ".join(filenames)
        assert f"error: unrecognized arguments: {filenames_string}" in (
            stderr.getvalue()
        )

    for filename in filenames:
        os.remove(filename)


@pytest.mark.parametrize(
    "files_kwargs",
    (
        {
            "help": "Foo bar help",
            "metavar": "ARCHIVOS",
        },
        {
            "dest": "filepaths",
        },
    ),
    ids=("help,metavar", "dest"),
)
def test_extend_argument_parser__files_kwargs(files_kwargs):
    parser = argparse.ArgumentParser()
    extend_argument_parser(
        parser,
        files_kwargs=files_kwargs,
        languages=False,
        personal_dict=False,
    )

    files_action = parser._optionals._actions[-1]

    for kwarg, value in files_kwargs.items():
        assert getattr(files_action, kwarg) == value


def test_FilesOrGlobsAction():
    parser = argparse.ArgumentParser()
    extend_argument_parser(
        parser,
        languages=False,
        personal_dict=False,
    )

    tempdir = tempfile.gettempdir()

    # one glob
    hunspellcheck_foo_tempdir = os.path.join(tempdir, "hunspellcheck-foo")
    if os.path.isdir(hunspellcheck_foo_tempdir):
        shutil.rmtree(hunspellcheck_foo_tempdir)
    os.mkdir(hunspellcheck_foo_tempdir)

    foo_filenames = [
        os.path.join(hunspellcheck_foo_tempdir, filename)
        for filename in ("bar.txt", "baz.py", "foo.txt")
    ]
    for filename in foo_filenames:
        with open(filename, "w") as f:
            f.write("")

    opts = parser.parse_args([os.path.join(hunspellcheck_foo_tempdir, "*.txt")])
    files = sorted(opts.files)
    assert len(files) == 2
    assert files[0] == foo_filenames[0]
    assert files[1] == foo_filenames[2]

    # multiple globs
    hunspellcheck_bar_tempdir = os.path.join(tempdir, "hunspellcheck-bar")
    if os.path.isdir(hunspellcheck_bar_tempdir):
        shutil.rmtree(hunspellcheck_bar_tempdir)
    os.mkdir(hunspellcheck_bar_tempdir)

    bar_filenames = [
        os.path.join(hunspellcheck_bar_tempdir, filename)
        for filename in ("bar.txt", "baz.py", "foo.txt")
    ]
    for filename in bar_filenames:
        with open(filename, "w") as f:
            f.write("")

    opts = parser.parse_args(
        [
            os.path.join(hunspellcheck_foo_tempdir, "*.txt"),
            os.path.join(hunspellcheck_bar_tempdir, "*.py"),
        ]
    )
    files = sorted(opts.files)
    assert len(files) == 3
    assert files[0] == bar_filenames[1]
    assert files[1] == foo_filenames[0]
    assert files[2] == foo_filenames[2]

    for dirpath in [hunspellcheck_foo_tempdir, hunspellcheck_bar_tempdir]:
        shutil.rmtree(dirpath)
