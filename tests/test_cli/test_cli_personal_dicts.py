"""Tests for '--personal-dict' option of hunspellcheck CLI."""

import argparse
import contextlib
import io
import os
import tempfile
import uuid

import pytest

from hunspellcheck.cli import extend_argument_parser


@pytest.mark.parametrize("personal_dicts", (True, False))
@pytest.mark.parametrize("option", ("-p", "--personal-dict"))
def test_extend_argument_parser__personal_dicts(personal_dicts, option):
    parser = argparse.ArgumentParser()
    extend_argument_parser(
        parser,
        personal_dicts=personal_dicts,
        languages=False,
        files=False,
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
def test_extend_argument_parser__personal_dicts_name_or_flags(
    personal_dicts_name_or_flags,
):
    parser = argparse.ArgumentParser()
    extend_argument_parser(
        parser,
        personal_dicts_name_or_flags=personal_dicts_name_or_flags,
        languages=False,
        files=False,
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
def test_extend_argument_parser__personal_dicts_kwargs(personal_dicts_kwargs):
    parser = argparse.ArgumentParser()

    extend_argument_parser(
        parser,
        personal_dicts_kwargs=personal_dicts_kwargs,
        languages=False,
        files=False,
    )

    personal_dicts_action = parser._optionals._actions[-1]

    for kwarg, value in personal_dicts_kwargs.items():
        assert getattr(personal_dicts_action, kwarg) == value


def test_PersonalDictionaryAction():
    parser = argparse.ArgumentParser()
    extend_argument_parser(
        parser,
        languages=False,
        files=False,
    )

    # existent file
    foo_dict_filename = tempfile.NamedTemporaryFile().name
    with open(foo_dict_filename, "w") as f:
        f.write("foo")

    opts = parser.parse_args(["-p", foo_dict_filename])
    assert len(opts.personal_dicts) == 1
    assert opts.personal_dicts[0] == foo_dict_filename

    # multiple files
    bar_dict_filename = tempfile.NamedTemporaryFile().name
    with open(bar_dict_filename, "w") as f:
        f.write("bar")

    opts = parser.parse_args(["-p", foo_dict_filename, "-p", bar_dict_filename])
    assert len(opts.personal_dicts) == 2
    assert opts.personal_dicts[0] == foo_dict_filename
    assert opts.personal_dicts[1] == bar_dict_filename

    # non existent file
    os.remove(foo_dict_filename)
    with pytest.raises(FileNotFoundError) as err:
        parser.parse_args(["-p", foo_dict_filename])
    assert f'Personal dictionary file not found at "{foo_dict_filename}"' in (
        str(err.value),
    )
