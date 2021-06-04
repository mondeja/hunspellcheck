import pytest

from hunspellcheck.word import looks_like_a_word_creator


@pytest.mark.parametrize(
    (
        "value",
        "digits_are_words",
        "words_can_contain_digits",
        "words_can_startswith_dash",
        "words_can_endswith_dash",
        "words_can_contain_dash",
        "expected_result",
    ),
    (
        ("15ello", False, True, False, False, True, True),
        ("15ello", False, False, False, False, True, False),
        ("hell0", False, True, False, False, True, True),
        ("hell0", False, False, False, False, True, False),
        ("he11o", False, True, False, False, True, True),
        ("he11o", False, False, False, False, True, False),
        ("123", False, True, False, False, True, False),
        ("321", True, True, False, False, True, True),
        ("", False, True, False, False, True, False),
        (None, False, True, False, False, True, False),
        ("-hello", False, True, False, False, True, False),
        ("-hello", False, True, True, False, True, True),
        ("hello-", False, True, True, False, True, False),
        ("he-llo", False, True, True, False, True, True),
        ("he-llo", False, True, True, False, False, False),
        ("hello-", False, True, False, False, True, False),
        ("hello-", False, True, False, True, True, True),
        ("hello-good", False, True, False, False, True, True),
        ("hello-good", False, True, True, True, False, False),
        ("hello", False, True, False, False, True, True),
        ("Hello", False, True, False, False, True, True),
    ),
)
def test_looks_like_a_word_creator(
    value,
    digits_are_words,
    words_can_contain_digits,
    words_can_startswith_dash,
    words_can_endswith_dash,
    words_can_contain_dash,
    expected_result,
):
    func = looks_like_a_word_creator(
        digits_are_words=digits_are_words,
        words_can_contain_digits=words_can_contain_digits,
        words_can_startswith_dash=words_can_startswith_dash,
        words_can_endswith_dash=words_can_endswith_dash,
        words_can_contain_dash=words_can_contain_dash,
    )
    assert func(value) == expected_result
