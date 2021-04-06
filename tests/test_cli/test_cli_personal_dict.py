"""Tests for '--personal-dict' option of hunspellcheck CLI."""

import argparse
import contextlib
import io
import tempfile

import pytest

from hunspellcheck.cli import extend_argument_parser


@pytest.mark.parametrize("personal_dict", (True, False))
@pytest.mark.parametrize("option", ("-p", "--personal-dict"))
def test_extend_argument_parser__personal_dict(personal_dict, option):
    parser = argparse.ArgumentParser()
    extend_argument_parser(
        parser,
        personal_dict=personal_dict,
        language=False
    )

    personal_dict_file = tempfile.NamedTemporaryFile()

    if personal_dict:
        opts = parser.parse_args([option, personal_dict_file.name])
        assert opts.personal_dict == personal_dict_file.name
    else:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            with pytest.raises(SystemExit):
                parser.parse_args([option, personal_dict_file.name])

        expected_message = (
            f"error: unrecognized arguments: {option} {personal_dict_file.name}"
        )
        assert expected_message in stderr.getvalue()
