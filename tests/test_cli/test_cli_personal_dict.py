"""Tests for '--personal-dict' option of hunspellcheck CLI."""

import argparse
import contextlib
import io
import os
import tempfile
import uuid

import pytest

from hunspellcheck.cli import extend_argument_parser


@pytest.mark.parametrize("personal_dict", (True, False))
@pytest.mark.parametrize("option", ("-p", "--personal-dict"))
def test_extend_argument_parser__personal_dict(personal_dict, option):
    parser = argparse.ArgumentParser()
    extend_argument_parser(
        parser,
        personal_dict=personal_dict,
        languages=False,
        files=False,
    )

    personal_dict_file = tempfile.NamedTemporaryFile()

    if personal_dict:
        opts = parser.parse_args([option, personal_dict_file.name])
        assert opts.personal_dict == personal_dict_file.name
    else:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), pytest.raises(SystemExit):
            parser.parse_args([option, personal_dict_file.name])

        expected_message = (
            f"error: unrecognized arguments: {option} {personal_dict_file.name}"
        )
        assert expected_message in stderr.getvalue()


@pytest.mark.parametrize(
    "personal_dict_args",
    (
        ["--pdict"],
        ["-d", "--dictionary"],
    ),
    ids=(
        "--pdict",
        "-d/--dictionary",
    ),
)
def test_extend_argument_parser__personal_dict_args(personal_dict_args):
    parser = argparse.ArgumentParser()
    extend_argument_parser(
        parser,
        personal_dict_args=personal_dict_args,
        languages=False,
        files=False,
    )

    personal_dict_file = tempfile.NamedTemporaryFile()

    # personal_dict options matching
    for personal_dict_arg in personal_dict_args:
        opts = parser.parse_args([personal_dict_arg, personal_dict_file.name])
        assert opts.personal_dict == personal_dict_file.name

    # personal dict option not matching
    option = uuid.uuid4().hex[:8]
    stderr = io.StringIO()
    with contextlib.redirect_stderr(stderr), pytest.raises(SystemExit):
        parser.parse_args([f"--{option}", personal_dict_file.name])

    expected_message = (
        f"error: unrecognized arguments: --{option} {personal_dict_file.name}\n"
    )
    assert expected_message in stderr.getvalue()


@pytest.mark.parametrize(
    "personal_dict_kwargs",
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
def test_extend_argument_parser__personal_dict_kwargs(personal_dict_kwargs):
    parser = argparse.ArgumentParser()

    extend_argument_parser(
        parser,
        personal_dict_kwargs=personal_dict_kwargs,
        languages=False,
        files=False,
    )

    personal_dict_action = parser._optionals._actions[-1]

    for kwarg, value in personal_dict_kwargs.items():
        assert getattr(personal_dict_action, kwarg) == value


def test_PersonalDictionaryAction():
    parser = argparse.ArgumentParser()
    extend_argument_parser(
        parser,
        languages=False,
        files=False,
    )

    # existent file
    dict_filename = tempfile.NamedTemporaryFile().name
    with open(dict_filename, "w") as f:
        f.write("foo")

    opts = parser.parse_args(["-p", dict_filename])
    assert opts.personal_dict == dict_filename

    os.remove(opts.personal_dict)

    # non existent file
    with pytest.raises(FileNotFoundError) as err:
        parser.parse_args(["-p", dict_filename])
    assert f'Personal dictionary file not found at "{dict_filename}"' in (
        str(err.value),
    )
