"""Tests for hunspell-related utilities of hunspell-checker."""

import contextlib
import io
import types
import sys

import pytest

from hunspell_checker.hunspell import (
    gen_available_dictionaries,
    list_available_dictionaries,
    print_available_dictionaries,
)

def assert_dictionaries_list(dicts_list):
    assert len(dicts_list) > 0
    for dictname in dicts_list:
        assert dictname
        assert isinstance(dictname, str)


def test_gen_available_dictionaries():
    available_dicts_gen =  gen_available_dictionaries()
    assert isinstance(available_dicts_gen, types.GeneratorType)
    assert_dictionaries_list(list(available_dicts_gen))


def test_list_available_dictionaries():
    assert_dictionaries_list(list_available_dictionaries())


@pytest.mark.parametrize("sort", (True, False))
@pytest.mark.parametrize(
    "stream",
    (
        lambda: sys.stdout,
        lambda: io.StringIO()
    ),
    ids=[
        "sys.stdout",
        "io.StringIO",
    ]
)
def test_print_available_dictionaries(sort, stream, capsys):
    _stream = stream()
    print_available_dictionaries(sort=sort, stream=_stream)

    if isinstance(_stream, type(sys.stdout)):
        stdout = capsys.readouterr().out
    else:
        stdout = _stream.getvalue()

    available_dictionaries_list = stdout.splitlines()
    expected_dictionaries_list = list_available_dictionaries()
    if sort:
        assert available_dictionaries_list == sorted(expected_dictionaries_list)
    else:
        assert available_dictionaries_list == expected_dictionaries_list
