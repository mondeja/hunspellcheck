"""Tests for '--personal-dict' option of hunspellcheck CLI."""

import argparse
import contextlib
import io
import os
import shutil
import tempfile
import uuid

import pytest

from hunspellcheck.cli import hunspellchecker_argument_parser


@pytest.mark.parametrize("personal_dicts", (True, False))
@pytest.mark.parametrize("option", ("-p", "--personal-dict"))
def test_hunspellchecker_argument_parser__personal_dicts(personal_dicts, option):
    parser = argparse.ArgumentParser()
    hunspellchecker_argument_parser(
        parser,
        personal_dicts=personal_dicts,
        languages=False,
        files=False,
        encoding=False,
    )

    personal_dicts_file = tempfile.NamedTemporaryFile()

    if personal_dicts:
        opts = parser.parse_args([option, personal_dicts_file.name])
        assert len(opts.personal_dicts) == 1
        assert opts.personal_dicts[0] == personal_dicts_file.name
    else:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), pytest.raises(SystemExit):
            parser.parse_args([option, personal_dicts_file.name])

        expected_message = (
            f"error: unrecognized arguments: {option} {personal_dicts_file.name}"
        )
        assert expected_message in stderr.getvalue()


@pytest.mark.parametrize(
    "personal_dicts_name_or_flags",
    (
        ["--pdict"],
        ["-d", "--dictionary"],
    ),
    ids=(
        "--pdict",
        "-d/--dictionary",
    ),
)
def test_hunspellchecker_argument_parser__personal_dicts_name_or_flags(
    personal_dicts_name_or_flags,
):
    parser = argparse.ArgumentParser()
    hunspellchecker_argument_parser(
        parser,
        personal_dicts_name_or_flags=personal_dicts_name_or_flags,
        languages=False,
        files=False,
        encoding=False,
    )

    personal_dicts_file = tempfile.NamedTemporaryFile()

    # personal_dicts options matching
    for personal_dicts_arg in personal_dicts_name_or_flags:
        opts = parser.parse_args([personal_dicts_arg, personal_dicts_file.name])
        assert len(opts.personal_dicts) == 1
        assert opts.personal_dicts[0] == personal_dicts_file.name

    # personal dict option not matching
    option = uuid.uuid4().hex[:8]
    stderr = io.StringIO()
    with contextlib.redirect_stderr(stderr), pytest.raises(SystemExit):
        parser.parse_args([f"--{option}", personal_dicts_file.name])

    expected_message = (
        f"error: unrecognized arguments: --{option} {personal_dicts_file.name}\n"
    )
    assert expected_message in stderr.getvalue()


@pytest.mark.parametrize(
    "personal_dicts_kwargs",
    (
        {
            "help": "Foo bar help",
            "metavar": "PERSONAL DICT",
        },
        {
            "dest": "custom_dictionary",
        },
    ),
    ids=("help,metavar", "dest"),
)
def test_hunspellchecker_argument_parser__personal_dicts_kwargs(personal_dicts_kwargs):
    parser = argparse.ArgumentParser()

    hunspellchecker_argument_parser(
        parser,
        personal_dicts_kwargs=personal_dicts_kwargs,
        languages=False,
        files=False,
        encoding=False,
    )

    personal_dicts_action = parser._optionals._actions[-14]

    for kwarg, value in personal_dicts_kwargs.items():
        assert getattr(personal_dicts_action, kwarg) == value


def test_PersonalDictionaryAction():
    parser = argparse.ArgumentParser()
    hunspellchecker_argument_parser(
        parser,
        languages=False,
        files=False,
        encoding=False,
    )

    # existent file
    foo_dict_filename = tempfile.NamedTemporaryFile().name
    with open(foo_dict_filename, "w") as f:
        f.write("foo")

    opts = parser.parse_args(["-p", foo_dict_filename])
    assert len(opts.personal_dicts) == 1
    assert opts.personal_dicts[0] == foo_dict_filename

    # multiple files by filepath
    bar_dict_filename = tempfile.NamedTemporaryFile().name
    with open(bar_dict_filename, "w") as f:
        f.write("bar")

    opts = parser.parse_args(["-p", foo_dict_filename, "-p", bar_dict_filename])
    assert len(opts.personal_dicts) == 2
    assert opts.personal_dicts[0] == foo_dict_filename
    assert opts.personal_dicts[1] == bar_dict_filename

    # non existent file
    os.remove(foo_dict_filename)
    os.remove(bar_dict_filename)
    opts = parser.parse_args(["-p", foo_dict_filename])
    assert len(opts.personal_dicts) == 0

    # multiple files by globs
    tempdir = tempfile.gettempdir()
    dicts_dirs = {"foo": None, "bar": None}
    for dirname in dicts_dirs:
        dicts_dir = os.path.join(tempdir, f"hunspellcheck-{dirname}")
        if os.path.isdir(dicts_dir):
            shutil.rmtree(dicts_dir)
        os.mkdir(dicts_dir)
        dicts_dirs[dirname] = dicts_dir
        for filename in ["foo.txt", "bar.txt"]:
            filepath = os.path.join(dicts_dir, filename)
            if os.path.isfile(filepath):
                os.remove(filepath)
            os.mknod(filepath)

    opts = parser.parse_args(
        [
            "-p",
            os.path.join(tempdir, "hunspellcheck-foo", "*.txt"),
            "-p",
            os.path.join(tempdir, "hunspellcheck-bar", "*.txt"),
        ]
    )
    assert len(opts.personal_dicts) == 4

    for dirname, dirpath in dicts_dirs.items():
        shutil.rmtree(dirpath)
