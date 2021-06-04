"""Tests for '-i/--input-encoding' option of hunspellcheck CLI utilities."""

import argparse
import contextlib
import io
import uuid

import pytest

from hunspellcheck.cli import hunspellchecker_argument_parser


@pytest.mark.parametrize("encoding", (True, False))
@pytest.mark.parametrize("option", ("-i", "--input-encoding"))
def test_hunspellchecker_argument_parser__encoding(encoding, option):
    """Test 'encoding' argument of 'hunspellchecker_argument_parser' function."""
    parser = argparse.ArgumentParser()
    hunspellchecker_argument_parser(
        parser,
        languages=False,
        personal_dicts=False,
        files=False,
        encoding=encoding,
    )

    if encoding:
        opts = parser.parse_args([option, "utf-8"])
        assert opts.encoding == "utf-8"
    else:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), pytest.raises(SystemExit):
            parser.parse_args([option, "utf-8"])
        assert f"error: unrecognized arguments: {option}" in stderr.getvalue()


@pytest.mark.parametrize(
    "encoding_name_or_flags",
    (
        ["--input"],
        ["-e", "--encoding"],
    ),
    ids=(
        "--input",
        "-e/--encoding",
    ),
)
def test_hunspellchecker_argument_parser__encoding_name_or_flags(
    encoding_name_or_flags,
):
    parser = argparse.ArgumentParser()
    hunspellchecker_argument_parser(
        parser,
        encoding_name_or_flags=encoding_name_or_flags,
        personal_dicts=False,
        files=False,
        languages=False,
    )

    # encodings option matching
    for encoding_arg in encoding_name_or_flags:
        opts = parser.parse_args([encoding_arg, "utf-8"])
        assert opts.encoding == "utf-8"

    # encoding option not matching
    stderr, option = (io.StringIO(), uuid.uuid4().hex[:8])
    with contextlib.redirect_stderr(stderr), pytest.raises(SystemExit):
        parser.parse_args([f"--{option}", "utf-8"])

    expected_message = f"error: unrecognized arguments: --{option} utf-8\n"
    assert expected_message in stderr.getvalue()


@pytest.mark.parametrize(
    "encoding_kwargs",
    (
        {
            "help": "Foo bar help",
            "metavar": "CODIFICACIÓN",
        },
        {
            "dest": "en_coding",
        },
    ),
    ids=("help,metavar", "dest"),
)
def test_hunspellchecker_argument_parser__encoding_kwargs(encoding_kwargs):
    parser = argparse.ArgumentParser()

    hunspellchecker_argument_parser(
        parser,
        encoding_kwargs=encoding_kwargs,
        personal_dicts=False,
        files=False,
        languages=False,
    )

    encoding_action = parser._optionals._actions[-14]

    for kwarg, value in encoding_kwargs.items():
        assert getattr(encoding_action, kwarg) == value
