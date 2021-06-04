"""Tests for '--version' option CLI utilities."""

import argparse
import contextlib
import io
import os
import re
import sys
import uuid

import pytest

from hunspellcheck.cli import hunspellchecker_argument_parser


@pytest.mark.parametrize("version", (True, False))
@pytest.mark.parametrize("option", ("--version",))
def test_hunspellchecker_argument_parser__version(version, option):
    parser = argparse.ArgumentParser()
    hunspellchecker_argument_parser(
        parser,
        version=version,
        languages=False,
        personal_dicts=False,
        files=False,
        encoding=False,
    )

    if version:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), pytest.raises(SystemExit):
            parser.parse_args([option])
        assert re.match(
            r"^Hunspell (\d+\.\d+\.\d+) - Ispell (\d+\.\d+\.\d+)", stdout.getvalue()
        )
    else:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), pytest.raises(SystemExit):
            parser.parse_args([option])
        assert f"error: unrecognized arguments: {option}" in stderr.getvalue()


@pytest.mark.parametrize(
    "version_name_or_flags",
    (
        ["--vers"],
        ["-v", "--give-me-the-version"],
    ),
    ids=(
        "--vers",
        "-v/--give-me-the-version",
    ),
)
def test_hunspellchecker_argument_parser__version_name_or_flags(version_name_or_flags):
    parser = argparse.ArgumentParser()
    hunspellchecker_argument_parser(
        parser,
        version=True,
        version_name_or_flags=version_name_or_flags,
        version_number="1.0.0",
        version_prog="foo",
        hunspell_version=False,
        ispell_version=False,
        files=False,
        languages=False,
        personal_dicts=False,
        encoding=False,
    )

    # version options matching
    for version_arg in version_name_or_flags:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), pytest.raises(SystemExit):
            parser.parse_args([version_arg])
        assert stdout.getvalue() == "foo 1.0.0\n"

    # version options not matching
    stderr, mismatching_option = (io.StringIO(), uuid.uuid4().hex[:8])
    with contextlib.redirect_stderr(stderr), pytest.raises(SystemExit):
        parser.parse_args([f"--{mismatching_option}"])
    assert f"error: unrecognized arguments: --{mismatching_option}" in (
        stderr.getvalue()
    )


@pytest.mark.parametrize(
    "version_kwargs",
    (
        {
            "help": "Foo bar help",
        },
        {
            "version": "0.5.1",
        },
    ),
    ids=("help,metavar", "dest"),
)
def test_hunspellchecker_argument_parser__version_kwargs(version_kwargs):
    parser = argparse.ArgumentParser()

    hunspellchecker_argument_parser(
        parser,
        version=True,
        version_kwargs=version_kwargs,
        files=False,
        languages=False,
        personal_dicts=False,
        encoding=False,
    )

    version_action = parser._optionals._actions[-6]
    for kwarg, value in version_kwargs.items():
        assert getattr(version_action, kwarg) == value


@pytest.mark.parametrize(
    (
        "version_number",
        "version_prog",
        "hunspell_version",
        "ispell_version",
        "regex_result",
    ),
    (
        # all parameters explicit
        (
            "0.0.1",
            "foo",
            True,
            True,
            r"foo 0\.0\.1 - Hunspell (\d+\.\d+\.\d+) - Ispell (\d+\.\d+\.\d+)",
        ),
        # without prog, prog obtained from argument parser (pytest entrypoint)
        (
            "0.0.1",
            None,
            True,
            True,
            (
                rf"^{os.path.basename(sys.argv[0])} 0\.0\.1 -"
                r" Hunspell (\d+\.\d+\.\d+) - Ispell (\d+\.\d+\.\d+)"
            ),
        ),
        # without version number, no prog neither version number
        (
            None,
            "foo",
            True,
            True,
            r"^Hunspell (\d+\.\d+\.\d+) - Ispell (\d+\.\d+\.\d+)",
        ),
        (
            None,
            None,
            True,
            True,
            r"^Hunspell (\d+\.\d+\.\d+) - Ispell (\d+\.\d+\.\d+)",
        ),
        # without hunspell version
        (
            "0.0.1",
            "foo",
            False,
            True,
            r"^foo 0\.0\.1 - Ispell (\d+\.\d+\.\d+)",
        ),
        (
            None,
            None,
            False,
            True,
            r"^Ispell (\d+\.\d+\.\d+)",
        ),
        # without ispell version
        (
            "0.0.1",
            "foo",
            True,
            False,
            r"^foo 0\.0\.1 - Hunspell (\d+\.\d+\.\d+)",
        ),
        (
            None,
            None,
            True,
            False,
            r"^Hunspell (\d+\.\d+\.\d+)",
        ),
        # only version nomber
        (
            "0.1.0",
            "bar",
            False,
            False,
            r"^bar 0\.1\.0",
        ),
        (
            "1.0.0",
            "baz",
            False,
            False,
            r"^baz 1\.0\.0",
        ),
        # any (--version option not included)
        (
            None,
            None,
            False,
            False,
            None,
        ),
    ),
)
def test_hunspellchecker_argument_parser__version_default_template(
    version_number,
    version_prog,
    hunspell_version,
    ispell_version,
    regex_result,
):
    parser = argparse.ArgumentParser()
    hunspellchecker_argument_parser_kwargs = dict(
        version=True,
        version_number=version_number,
        version_prog=version_prog,
        hunspell_version=hunspell_version,
        ispell_version=ispell_version,
        files=False,
        languages=False,
        personal_dicts=False,
        encoding=False,
    )

    # any ('--version' option not included)
    if not any([version_number, hunspell_version, ispell_version]):
        with pytest.warns(UserWarning) as record:
            hunspellchecker_argument_parser(
                parser, **hunspellchecker_argument_parser_kwargs
            )
        assert record[0].message.args[0] == (
            "'--version' option not added because version string is empty!"
        )

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), pytest.raises(SystemExit):
            parser.parse_args(["--version"])
        assert "error: unrecognized arguments: --version" in stderr.getvalue()
    else:
        hunspellchecker_argument_parser(
            parser, **hunspellchecker_argument_parser_kwargs
        )

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), pytest.raises(SystemExit):
            parser.parse_args(["--version"])
        assert re.match(regex_result, stdout.getvalue())
