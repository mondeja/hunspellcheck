"""Tests for hunspell-related utilities about dictionaries."""

import io
import os
import sys
import types

import pytest

from hunspellcheck.exceptions import InvalidLanguageDictionaryError
from hunspellcheck.hunspell.dictionaries import (
    assert_is_valid_dictionary_language_or_filename,
    gen_available_dictionaries,
    is_valid_dictionary_language_or_filename,
    list_available_dictionaries,
    print_available_dictionaries,
)


VALID_DICTIONARY_LANGUAGE = list_available_dictionaries()[0]


def assert_dictionaries_list(dicts_list, full_paths=False):
    assert len(dicts_list) > 0
    for dictname in dicts_list:
        assert dictname
        assert isinstance(dictname, str)
        if full_paths:
            assert os.path.isfile(f"{dictname}.dic")


@pytest.mark.parametrize("full_paths", (True, False))
def test_gen_available_dictionaries(full_paths):
    available_dicts_gen = gen_available_dictionaries(full_paths=full_paths)
    assert isinstance(available_dicts_gen, types.GeneratorType)
    assert_dictionaries_list(list(available_dicts_gen), full_paths=full_paths)


@pytest.mark.parametrize("full_paths", (True, False))
def test_list_available_dictionaries(full_paths):
    assert_dictionaries_list(
        list_available_dictionaries(full_paths=full_paths), full_paths=full_paths
    )


@pytest.mark.parametrize("sort", (True, False))
@pytest.mark.parametrize(
    "stream",
    (lambda: sys.stdout, lambda: io.StringIO()),
    ids=[
        "sys.stdout",
        "io.StringIO",
    ],
)
@pytest.mark.parametrize("full_paths", (True, False))
def test_print_available_dictionaries(sort, stream, capsys, full_paths):
    _stream = stream()
    print_available_dictionaries(
        sort=sort,
        stream=_stream,
        full_paths=full_paths,
    )

    if isinstance(_stream, type(sys.stdout)):
        stdout = capsys.readouterr().out
    else:
        stdout = _stream.getvalue()

    available_dictionaries_list = stdout.splitlines()
    expected_dictionaries_list = list_available_dictionaries(full_paths=full_paths)
    if sort:
        assert available_dictionaries_list == sorted(expected_dictionaries_list)
    else:
        assert available_dictionaries_list == expected_dictionaries_list


@pytest.mark.parametrize(
    ("value", "expected_result"),
    (
        ("setup.py", True),
        ("foobarbazimpossible.totallycrazyname", False),
        (VALID_DICTIONARY_LANGUAGE, True),
    ),
)
def test_is_valid_dictionary_language_or_filename(value, expected_result):
    assert is_valid_dictionary_language_or_filename(value) == expected_result


@pytest.mark.parametrize(
    ("value", "expected_error"),
    (
        (VALID_DICTIONARY_LANGUAGE, None),
        ("foobar.totallycrazyname", InvalidLanguageDictionaryError),
        (["barbaz.totallycrazyname"], InvalidLanguageDictionaryError),
    ),
)
def test_assert_is_valid_dictionary_language_or_filename(value, expected_error):
    if expected_error is None:
        assert_is_valid_dictionary_language_or_filename(value)
    else:
        with pytest.raises(expected_error) as exc:
            assert_is_valid_dictionary_language_or_filename(value)
        assert (value if isinstance(value, str) else value[0]) in str(exc.value)
