"""Tests for hunspell-related utilities of hunspellcheck."""

import contextlib
import io
import os
import types
import sys

import pytest

from hunspellcheck.hunspell import (
    gen_available_dictionaries,
    list_available_dictionaries,
    print_available_dictionaries,
)

def assert_dictionaries_list(dicts_list, full_paths=False):
    assert len(dicts_list) > 0
    for dictname in dicts_list:
        assert dictname
        assert isinstance(dictname, str)
        if full_paths:
            assert os.path.isfile(f"{dictname}.dic")


@pytest.mark.parametrize("full_paths", (True, False))
def test_gen_available_dictionaries(full_paths):
    available_dicts_gen =  gen_available_dictionaries(full_paths=full_paths)
    assert isinstance(available_dicts_gen, types.GeneratorType)
    assert_dictionaries_list(list(available_dicts_gen), full_paths=full_paths)


@pytest.mark.parametrize("full_paths", (True, False))
def test_list_available_dictionaries(full_paths):
    assert_dictionaries_list(
        list_available_dictionaries(full_paths=full_paths),
        full_paths=full_paths
    )



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
    expected_dictionaries_list = list_available_dictionaries(
        full_paths=full_paths
    )
    if sort:
        assert available_dictionaries_list == sorted(expected_dictionaries_list)
    else:
        assert available_dictionaries_list == expected_dictionaries_list
