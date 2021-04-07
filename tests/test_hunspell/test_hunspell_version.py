"""Tests for hunspell-related utilities about Hunspell versions."""

import re

import pytest

from hunspellcheck.hunspell.version import get_hunspell_version


@pytest.mark.parametrize(
    ("kwargs", "error"),
    (
        ({"hunspell": True, "ispell": True}, None),
        ({"hunspell": True, "ispell": False}, None),
        ({"hunspell": False, "ispell": True}, None),
        ({"hunspell": False, "ispell": False}, ValueError),
    ),
    ids=(
        "hunspell=True,ispell=True",
        "hunspell=True,ispell=False",
        "hunspell=False,ispell=True",
        "hunspell=False,ispell=False",
    ),
)
def test_get_hunspell_version(kwargs, error):
    if error is not None:
        with pytest.raises(error):
            get_hunspell_version(**kwargs)
    else:
        response = get_hunspell_version(**kwargs)

        for kwarg, value in kwargs.items():
            if value:
                assert kwarg in response
                assert isinstance(response[kwarg], str)
                assert re.match(r"^\d+\.\d+\.\d+", response[kwarg])
            else:
                assert response.get(kwarg) is None
