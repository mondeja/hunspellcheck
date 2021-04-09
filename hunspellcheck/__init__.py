"""Hunspellcheck package."""

from hunspellcheck.cli import extend_argument_parser
from hunspellcheck.hunspell.dictionaries import (
    gen_available_dictionaries,
    gen_available_dictionaries_with_langcodes,
    is_valid_dictionary_language,
    list_available_dictionaries,
    print_available_dictionaries,
)
from hunspellcheck.hunspell.version import get_hunspell_version
from hunspellcheck.spellchecker import HunspellChecker, render_hunspell_word_error


__version__ = "0.0.2"
__title__ = "hunspellcheck"
__all__ = (
    "extend_argument_parser",
    "gen_available_dictionaries",
    "gen_available_dictionaries_with_langcodes",
    "get_hunspell_version",
    "is_valid_dictionary_language",
    "list_available_dictionaries",
    "print_available_dictionaries",
    "render_hunspell_word_error",
    "HunspellChecker",
)
