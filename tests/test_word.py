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
        "words_can_contain_two_upper",
        "expected_result",
    ),
    (
        ("15ello", False, True, False, False, True, True, True),
        ("15ello", False, False, False, False, True, True, False),
        ("hell0", False, True, False, False, True, True, True),
        ("hell0", False, False, False, False, True, True, False),
        ("he11o", False, True, False, False, True, True, True),
        ("he11o", False, False, False, False, True, True, False),
        ("123", False, True, False, False, True, True, False),
        ("321", True, True, False, False, True, True, True),
        ("", False, True, False, False, True, True, False),
        (None, False, True, False, False, True, True, False),
        ("-hello", False, True, False, False, True, True, False),
        ("-hello", False, True, True, False, True, True, True),
        ("hello-", False, True, True, False, True, True, False),
        ("he-llo", False, True, True, False, True, True, True),
        ("he-llo", False, True, True, False, False, True, False),
        ("hello-", False, True, False, False, True, True, False),
        ("hello-", False, True, False, True, True, True, True),
        ("hello-good", False, True, False, False, True, True, True),
        ("hello-good", False, True, True, True, False, True, False),
        ("hello", False, True, False, False, True, True, True),
        ("Hello", False, True, False, False, True, True, True),
        ("HEllo", False, True, False, False, True, True, True),
        ("HEllo", False, True, False, False, True, False, False),
        ("hELLo", False, True, False, False, True, False, False),
        ("hELLo", False, True, False, False, True, True, True),
        ("hE11o", False, True, False, False, True, False, True),
    ),
)
def test_looks_like_a_word_creator(
    value,
    digits_are_words,
    words_can_contain_digits,
    words_can_startswith_dash,
    words_can_endswith_dash,
    words_can_contain_dash,
    words_can_contain_two_upper,
    expected_result,
):
    func = looks_like_a_word_creator(
        digits_are_words=digits_are_words,
        words_can_contain_digits=words_can_contain_digits,
        words_can_startswith_dash=words_can_startswith_dash,
        words_can_endswith_dash=words_can_endswith_dash,
        words_can_contain_dash=words_can_contain_dash,
        words_can_contain_two_upper=words_can_contain_two_upper,
    )
    assert func(value) == expected_result
