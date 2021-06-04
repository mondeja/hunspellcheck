"""CLI language-related utilities tests for hunspellcheck."""

import argparse
import contextlib
import io
import uuid

import pytest
from babel import Locale

from hunspellcheck.cli import hunspellchecker_argument_parser
from hunspellcheck.hunspell.dictionaries import (
    gen_available_dictionaries,
    list_available_dictionaries,
)


@pytest.mark.parametrize("languages", (True, False))
@pytest.mark.parametrize("option", ("-l", "--language"))
def test_hunspellchecker_argument_parser__languages(languages, option):
    """Test 'language' argument of 'hunspellchecker_argument_parser' function."""
    parser = argparse.ArgumentParser()
    hunspellchecker_argument_parser(
        parser,
        languages=languages,
        personal_dicts=False,
        files=False,
        encoding=False,
    )

    if languages:
        opts = parser.parse_args([option, "en_US"])
        assert len(opts.languages) == 1
        assert opts.languages[0] == "en_US"

        # multiple languages
        opts = parser.parse_args([option, "en_US", option, "en_AU"])
        assert len(opts.languages) == 2
        assert opts.languages[0] == "en_US"
        assert opts.languages[1] == "en_AU"
    else:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), pytest.raises(SystemExit):
            parser.parse_args([option, "en_US"])
        assert f"error: unrecognized arguments: {option} en_US" in stderr.getvalue()


@pytest.mark.parametrize(
    "languages_name_or_flags",
    (
        ["--lang"],
        ["-d", "--dictionary"],
    ),
    ids=(
        "--lang",
        "-d/--dictionary",
    ),
)
def test_hunspellchecker_argument_parser__languages_name_or_flags(
    languages_name_or_flags,
):
    parser = argparse.ArgumentParser()
    hunspellchecker_argument_parser(
        parser,
        languages_name_or_flags=languages_name_or_flags,
        personal_dicts=False,
        files=False,
        encoding=False,
    )

    # language options matching
    for languages_arg in languages_name_or_flags:
        opts = parser.parse_args([languages_arg, "en_US"])
        assert len(opts.languages) == 1
        assert opts.languages[0] == "en_US"

    # language options not matching
    stderr = io.StringIO()
    with contextlib.redirect_stderr(stderr), pytest.raises(SystemExit):
        parser.parse_args([f"--{uuid.uuid4().hex[:8]}", "en_US"])

    args_string = "/".join(languages_name_or_flags)
    expected_message = f"the following arguments are required: {args_string}"
    assert expected_message in stderr.getvalue()


@pytest.mark.parametrize(
    "languages_kwargs",
    (
        {
            "help": "Foo bar help",
            "metavar": "IDIOMA",
        },
        {
            "dest": "idioma",
        },
    ),
    ids=("help,metavar", "dest"),
)
def test_hunspellchecker_argument_parser__languages_kwargs(languages_kwargs):
    parser = argparse.ArgumentParser()

    hunspellchecker_argument_parser(
        parser,
        languages_kwargs=languages_kwargs,
        personal_dicts=False,
        files=False,
        encoding=False,
    )

    language_action = parser._optionals._actions[-15]

    for kwarg, value in languages_kwargs.items():
        assert getattr(language_action, kwarg) == value


@pytest.mark.parametrize("negotiate_languages", (True, False))
def test_hunspellchecker_argument_parser__negotiate_languages(negotiate_languages):
    parser = argparse.ArgumentParser()
    hunspellchecker_argument_parser(
        parser,
        negotiate_languages=negotiate_languages,
        personal_dicts=False,
        files=False,
        encoding=False,
    )

    if negotiate_languages:
        opts = parser.parse_args(["--language", "en"])
        assert len(opts.languages) == 1
        assert opts.languages[0].startswith("en")
    else:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), pytest.raises(SystemExit):
            parser.parse_args(["--language", "en"])
        assert "error: argument -l/--language: invalid choice: 'en'" in (
            stderr.getvalue()
        )


def test_HunspellDictionaryNegotiatorAction():
    parser = argparse.ArgumentParser()
    hunspellchecker_argument_parser(
        parser,
        negotiate_languages=True,
        personal_dicts=False,
        files=False,
        encoding=False,
    )

    # language negotiation 'en' -> 'en_US' (depends on available dictionaries)
    lang_code = "en"
    opts = parser.parse_args(["-l", lang_code])
    assert len(opts.languages) == 1
    assert opts.languages[0] == str(
        Locale.negotiate([lang_code], list_available_dictionaries())
    )

    # invalid language dictionary
    lang_code = "jnfdsmfbs"
    stderr = io.StringIO()
    with contextlib.redirect_stderr(stderr), pytest.raises(SystemExit):
        parser.parse_args(["-l", lang_code])
    assert (
        f"argument -l/--language: invalid choice: '{lang_code}' (choose from '"
    ) in stderr.getvalue()

    # language dictionary by filename
    language_action = parser._optionals._actions[-15]
    language_action.choices = None

    dictionary_full_path = next(gen_available_dictionaries(full_paths=True))
    dictionary_filename = f"{dictionary_full_path}.dic"
    opts = parser.parse_args(["-l", dictionary_filename])
    assert len(opts.languages) == 1
    assert opts.languages[0] == dictionary_full_path
