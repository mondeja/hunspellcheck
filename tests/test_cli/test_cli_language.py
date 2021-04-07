"""CLI language-related utilities tests for hunspellcheck."""

import argparse
import contextlib
import io
import uuid

import pytest
from babel import Locale

from hunspellcheck.cli import extend_argument_parser
from hunspellcheck.cli.language import HunspellDictionaryNegotiatorAction
from hunspellcheck.hunspell.dictionaries import (
    gen_available_dictionaries,
    list_available_dictionaries,
)


@pytest.mark.parametrize("language", (True, False))
@pytest.mark.parametrize("option", ("-l", "--languages"))
def test_extend_argument_parser__language(language, option):
    """Test 'language' argument of 'extend_argument_parser' function."""
    parser = argparse.ArgumentParser()
    extend_argument_parser(
        parser,
        language=language,
        personal_dict=False,
        files=False,
    )

    if language:
        opts = parser.parse_args([option, "en_US"])
        assert len(opts.language) == 1
        assert opts.language[0] == "en_US"

        # multiple languages
        opts = parser.parse_args([option, "en_US", option, "en_AU"])
        assert len(opts.language) == 2
        assert opts.language[0] == "en_US"
        assert opts.language[1] == "en_AU"
    else:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), pytest.raises(SystemExit):
            parser.parse_args([option, "en_US"])
        assert f"error: unrecognized arguments: {option} en_US" in stderr.getvalue()


@pytest.mark.parametrize(
    "language_args",
    (
        ["--lang"],
        ["-d", "--dictionary"],
    ),
    ids=(
        "--lang",
        "-d/--dictionary",
    ),
)
def test_extend_argument_parser__language_args(language_args):
    parser = argparse.ArgumentParser()
    extend_argument_parser(
        parser,
        language_args=language_args,
        personal_dict=False,
        files=False,
    )

    # language options matching
    for language_arg in language_args:
        opts = parser.parse_args([language_arg, "en_US"])
        assert len(opts.language) == 1
        assert opts.language[0] == "en_US"

    # language options not matching
    stderr = io.StringIO()
    with contextlib.redirect_stderr(stderr), pytest.raises(SystemExit):
        parser.parse_args([f"--{uuid.uuid4().hex[:8]}", "en_US"])

    args_string = "/".join(language_args)
    expected_message = f"the following arguments are required: {args_string}"
    assert expected_message in stderr.getvalue()


@pytest.mark.parametrize(
    "language_kwargs",
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
def test_extend_argument_parser__language_kwargs(language_kwargs):
    parser = argparse.ArgumentParser()

    extend_argument_parser(
        parser,
        language_kwargs=language_kwargs,
        personal_dict=False,
        files=False,
    )

    language_action = parser._optionals._actions[-1]

    for kwarg, value in language_kwargs.items():
        assert getattr(language_action, kwarg) == value


@pytest.mark.parametrize(
    ("negotiate_language", "action_class"),
    (
        (True, HunspellDictionaryNegotiatorAction),
        (False, argparse._ExtendAction),
    ),
)
def test_extend_argument_parser__negotiate_language(
    negotiate_language,
    action_class,
):
    parser = argparse.ArgumentParser()
    extend_argument_parser(
        parser,
        negotiate_language=negotiate_language,
        personal_dict=False,
        files=False,
    )

    language_action = parser._optionals._actions[-1]
    assert isinstance(language_action, action_class)


def test_HunspellDictionaryNegotiatorAction():
    parser = argparse.ArgumentParser()
    extend_argument_parser(
        parser,
        negotiate_language=True,
        personal_dict=False,
        files=False,
    )

    # language negotiation 'en' -> 'en_US' (depends on available dictionaries)
    lang_code = "en"
    opts = parser.parse_args(["-l", lang_code])
    assert len(opts.language) == 1
    assert opts.language[0] == str(
        Locale.negotiate([lang_code], list_available_dictionaries())
    )

    # invalid language dictionary
    lang_code = "jnfdsmfbs"
    stderr = io.StringIO()
    with contextlib.redirect_stderr(stderr), pytest.raises(SystemExit):
        parser.parse_args(["-l", lang_code])
    assert (
        f"argument -l/--languages: invalid choice: '{lang_code}' (choose from '"
    ) in stderr.getvalue()

    # language dictionary by filename
    language_action = parser._optionals._actions[-1]
    language_action.choices = None

    dictionary_full_path = next(gen_available_dictionaries(full_paths=True))
    dictionary_filename = f"{dictionary_full_path}.dic"
    opts = parser.parse_args(["-l", dictionary_filename])
    assert len(opts.language) == 1
    assert opts.language[0] == dictionary_full_path
