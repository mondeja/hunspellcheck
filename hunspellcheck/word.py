import string  # noqa: F401
import unicodedata  # noqa: F401


def looks_like_a_word_creator(
    digits_are_words=False,
    words_can_contain_digits=True,
    words_can_startswith_dash=True,
    words_can_endswith_dash=True,
    words_can_contain_dash=True,
    words_can_contain_two_upper=True,
):
    """Generates dinamically the function ``look_like_a_word`` use to clean the
    words that must not be checked for mispelling errors.

    Args:
        digits_are_words (bool): If ``False``, values with all characters as
            digits will not be considered words.
        words_can_contain_digits (bool): If ``False``, values with at least one
            digit character will not be considered words.
        words_can_startswith_dash (bool): If ``False``, values starting with the ``-``
            character will not be considered words.
        words_can_endswith_dash (bool): If ``False``, values ending with the ``-``
            character will not be considered words.
        words_can_contain_dash (bool): If ``False``, values containing the ``-``
            character will not be considered words.
        words_can_contain_two_upper (bool): If ``False``, values which
            contain at least two uppercase like CPython will not be considered
            words and will not be checking for possible mispellings.

    Returns:
        function: Function that takes a possible word as a parameter and
            returns if that value is considered a word. This function can be
            passed to :py:class:`hunspellcheck.spellchecker.HunspellChecker`.
    """
    conditions = [
        (digits_are_words, "all(char in string.digits for char in text)"),
        (words_can_contain_digits, "any(digit in text for digit in string.digits)"),
        (words_can_startswith_dash, 'text.startswith("-")'),
        (words_can_endswith_dash, 'text.endswith("-")'),
        (words_can_contain_dash, '"-" in text'),
        (
            words_can_contain_two_upper,
            'len([c for c in text if unicodedata.category(c) == "Lu"]) > 1',
        ),
    ]

    function_conditional = "if not text or "

    for i, (argument, condition) in enumerate(conditions):
        if argument is False:
            if not function_conditional.endswith(" or "):
                function_conditional += " or "
            function_conditional += condition
    function_conditional += ":\n        return False\n    "

    function_definition = f"""def looks_like_a_word(text):
    {function_conditional}return True"""

    code = compile(function_definition, "test", "exec")
    exec(code)
    return locals()["looks_like_a_word"]
