"""CLI utilities writing spell checkers."""

import warnings

from hunspellcheck.cli.files import FilesOrGlobsAction
from hunspellcheck.cli.languages import create_hunspell_valid_dictionary_action
from hunspellcheck.cli.personal_dicts import PersonalDictionaryAction
from hunspellcheck.cli.version import DEFAULT_VERSION_TEMPLATE, render_version_template


def hunspellchecker_argument_parser(
    parser,
    version=False,
    version_prog=None,
    version_number=None,
    hunspell_version=True,
    ispell_version=True,
    version_template=DEFAULT_VERSION_TEMPLATE,
    version_template_context={},
    version_name_or_flags=["--version"],
    version_kwargs={},
    files=True,
    files_kwargs={},
    languages=True,
    languages_name_or_flags=["-l", "--language"],
    languages_kwargs={},
    negotiate_languages=True,
    personal_dicts=True,
    personal_dicts_name_or_flags=["-p", "--personal-dict"],
    personal_dicts_kwargs={},
    encoding=True,
    encoding_name_or_flags=["-i", "--input-encoding"],
    encoding_kwargs={},
    digits_are_words=True,
    digits_are_words_name_or_flags=["--digits-are-words"],
    digits_are_words_kwargs={},
    words_not_contain_digits=True,
    words_not_contain_digits_name_or_flags=["--words-not-contain-digits"],
    words_not_contain_digits_kwargs={},
    words_not_startswith_dash=True,
    words_not_startswith_dash_name_or_flags=["--words-not-startswith-dash"],
    words_not_startswith_dash_kwargs={},
    words_not_endswith_dash=True,
    words_not_endswith_dash_name_or_flags=["--words-not-endswith-dash"],
    words_not_endswith_dash_kwargs={},
    words_not_contain_dash=True,
    words_not_contain_dash_name_or_flags=["--words-not-contain-dash"],
    words_not_contain_dash_kwargs={},
    words_not_contain_two_upper=True,
    words_not_contain_two_upper_name_or_flags=["--words-not-contain-two-upper"],
    words_not_contain_two_upper_kwargs={},
    no_include_filename=True,
    no_include_filename_name_or_flags=["--no-include-filename"],
    no_include_filename_kwargs={},
    no_include_line_number=True,
    no_include_line_number_name_or_flags=["--no-include-line-number"],
    no_include_line_number_kwargs={},
    no_include_word=True,
    no_include_word_name_or_flags=["--no-include-word"],
    no_include_word_kwargs={},
    no_include_word_line_index=True,
    no_include_word_line_index_name_or_flags=["--no-include-word-line-index"],
    no_include_word_line_index_kwargs={},
    include_line=True,
    include_line_name_or_flags=["--include-line"],
    include_line_kwargs={},
    include_text=True,
    include_text_name_or_flags=["--include-text"],
    include_text_kwargs={},
    include_error_number=True,
    include_error_number_name_or_flags=["--include-error-number"],
    include_error_number_kwargs={},
    include_near_misses=True,
    include_near_misses_name_or_flags=["--include-near-misses"],
    include_near_misses_kwargs={},
):
    """Extends a :py:class:`argparse.ArgumentParser` instance adding
    spellchecking common parameters.

    By default will add next parameters:

    * A positional argument as a property named ``files`` inside the options
      namespace which takes multiple possible globs as inputs.
    * A required argument ``-l/--language`` that could be passed multiple times
      which take language dictionary names or filepaths. It will check if the
      passed language is recognized by Hunspell (or if is a dictionary file, if
      exists), and in case that not, will print a list with all available
      dictionaries.
    * An optional argument ``-p/--personal-dict`` that could be passed multiple
      times which takes a path to a file used to exclude certain words from
      being triggered as positives.
    * An optional argument ``-i/--input-encoding`` that should define the input
      content encoding.

    Args:
        version (bool): Include a convenient ``--version`` option that will
            print the version of the program, and optionally the installed
            versions of Hunspell and Ispell. See ``version_prog``,
            ``version_number``, ``hunspell_version`` and ``ispell_version``
            parameters below.
        version_prog (str): Name of the program shown along the version. If is
            not provided, will be taken from ``parser.prog`` property.
        version_number (str): Version of the program. See ``version_template``
            argument below for details about the formatting.
        hunspell_version (str): Include version of Hunspell in the version
            shown passing ``--version``.
        ispell_version (str): Include version of Ispell in the version shown
            passing ``--version``.
        version_template (str): Template for version rendering passed to a
            :py:class:`jinja2.Template` object that will be used to renderize
            the version string. By default, if ``version_number`` is provided,
            and ``hunspell_version`` and ``ispell_version`` are ``True``,
            it will render a string like
            ``"<version_prog> <X.Y.Z> - Hunspell <X.Y.Z> - Ispell <X.Y.Z>"``.
            The data for template rendering by default is compound by the next
            fields: ``version_prog``, ``version_number``, ``hunspell_version``
            and ``ispell_version``. If you want to pass other fields, include
            them in the argument ``version_template_context``.
        version_template_context (dict): Additional data to use in the version
            string rendering.
        version_name_or_flags (list, str): Flag name defined constructing the
            ``--version`` argument using the method
            :py:meth:`argparse.ArgumentParser.add_argument`.
        version_kwargs (dict): Optional kwargs which override the default
            kwargs passed to :py:meth:`argparse.ArgumentParser.add_argument`
            constructing the ``--version`` option.
        files (bool): Include the ``files`` positional argument inside the
            argument parser.
        files_kwargs (dict): Optional kwargs which override the default
            kwargs passed to :py:meth:`argparse.ArgumentParser.add_argument`
            constructing the ``files`` positional argument.
        languages (bool): Include the ``-l/--language`` option inside the
            argument parser.
        languages_name_or_flags (list, str): Flag name defined constructing the
            ``-l/--language`` option using the method
            :py:meth:`argparse.ArgumentParser.add_argument`.
        languages_kwargs (dict): Optional kwargs which override the default
            kwargs passed to :py:meth:`argparse.ArgumentParser.add_argument`
            constructing the ``-l/--language`` option.
        negotiate_languages (bool): Enables the language negotiation. If this
            is enabled and the CLI consumer passes a locale code instead of
            a full language name (for example ``es`` instead of ``es_ES``),
            hunspellcheck will convert ``es`` to a territorialized language
            dictionary name available using the function
            :py:meth:`babel.core.Locale.negotiate`. If is disabled, a language
            dictionary passed as locale code like ``es`` will be considered
            invalid.
        personal_dicts (bool): Include the ``-p/--personal-dict`` option inside
            the argument parser.
        personal_dicts_name_or_flags (list, str): Flag name defined constructing
            the ``-p/--personal-dict`` option using the method
            :py:meth:`argparse.ArgumentParser.add_argument`.
        personal_dicts_kwargs (dict): Optional kwargs which override the default
            kwargs passed to :py:meth:`argparse.ArgumentParser.add_argument`
            constructing the ``-p/--personal-dict`` option.
        encoding (bool): Include the ``-i/--input-encoding`` hunspell option
            inside the argument parser.
        encoding_name_or_flags (list, str): Flag name defined constructing
            the ``-i/--input-encoding`` option using the method
            :py:meth:`argparse.ArgumentParser.add_argument`.
        encoding_kwargs (dict): Optional kwargs which override the default
            kwargs passed to :py:meth:`argparse.ArgumentParser.add_argument`
            building the ``-i/--input-encoding`` option.
        digits_are_words (bool): Include the option ``--digits-are-words`` to
            define if a value filled by digits will be considered a word for
            mispellchecking or not.
        digits_are_words_name_or_flags (list, str): Flag name defined
            constructing the ``--digits-are-words`` option using the method
            :py:meth:`argparse.ArgumentParser.add_argument`.
        digits_are_words_kwargs (dict): Optional kwargs which override default
            kwargs passed to :py:meth:`argparse.ArgumentParser.add_argument`
            building the ``--digits-are-words`` option.
        words_not_contain_digits (bool): Include the option
            ``--words-not-contain-digits`` which when passed in a CLI, the
            words that contain digits will be ignored mispellchecking errors.
        words_not_contain_digits_name_or_flags (list): Flag name defined
            constructing the ``--words-not-contain-digits`` option using the
            method :py:meth:`argparse.ArgumentParser.add_argument`.
        words_not_contain_digits_kwargs (dict): Optional kwargs which override
            default kwargs passed to
            :py:meth:`argparse.ArgumentParser.add_argument` building the
            ``--words-not-contain-digits`` option.
        words_not_startswith_dash (bool): Include the option
            ``--words-not-startswith-dash`` which when passed in a CLI, the
            words starting with character ``"-" `` will be ignored
            mispellchecking errors.
        words_not_startswith_dash_name_or_flags (list): Flag name defined
            constructing the ``--words-not-startswith-dash`` option using the
            method :py:meth:`argparse.ArgumentParser.add_argument`.
        words_not_startswith_dash_kwargs (dict): Optional kwargs which override
            default kwargs passed to
            :py:meth:`argparse.ArgumentParser.add_argument` building the
            ``--words-not-startswith-dash`` option.
        words_not_endswith_dash (bool): Include the option
            ``--words-not-endswith-dash`` which when passed in a CLI, the
            words ending with character ``"-" `` will be ignored
            mispellchecking errors.
        words_not_endswith_dash_name_or_flags (list): Flag name defined
            constructing the ``--words-not-endswith-dash`` option using the
            method :py:meth:`argparse.ArgumentParser.add_argument`.
        words_not_endswith_dash_kwargs (dict): Optional kwargs which override
            default kwargs passed to
            :py:meth:`argparse.ArgumentParser.add_argument` building the
            ``--words-not-endswith-dash`` option.
        words_not_contain_dash (bool): Include the option
            ``--words-not-contain-dash`` which when passed in a CLI, the
            words containing character ``"-" `` will be ignored mispellchecking
            for possible errors.
        words_not_contain_dash_name_or_flags (list): Flag name defined
            constructing the ``--words-not-contain-dash`` option using the
            method :py:meth:`argparse.ArgumentParser.add_argument`.
        words_not_contain_dash_kwargs (dict): Optional kwargs which override
            default kwargs passed to
            :py:meth:`argparse.ArgumentParser.add_argument` building the
            ``--words-not-contain-dash`` option.
        words_not_contain_two_upper (bool): Include the option
            ``--words-not-contain-two-upper`` which when passed in a CLI, the
            words containing two uppercase letters or mote will be ignored
            mispellchecking for possible errors.
        words_not_contain_two_upper_name_or_flags (list): Flag name defined
            constructing the ``--words-not-contain-two-upper`` option using the
            method :py:meth:`argparse.ArgumentParser.add_argument`.
        words_not_contain_two_upper_kwargs (dict): Optional kwargs which override
            default kwargs passed to
            :py:meth:`argparse.ArgumentParser.add_argument` building the
            ``--words-not-contain-two-upper`` option.
        no_include_filename (bool): Include the option
            ``--no-include-filename`` which when passed in a CLI, the path to
            files in which mispelling errors are found are not shown in
            the output.
        no_include_filename_name_or_flags (list): Flag name defined
            constructing the ``--no-include-filename`` option using the
            method :py:meth:`argparse.ArgumentParser.add_argument`.
        no_include_filename_kwargs (dict): Optional kwargs which override
            default kwargs passed to
            :py:meth:`argparse.ArgumentParser.add_argument` building the
            ``--no-include-filename`` option.
        no_include_line_number (bool): Include the option
            ``--no-include-line-number`` which when passed in a CLI, the number
            of lines in which mispelling errors are found are not shown in
            the output.
        no_include_line_number_name_or_flags (list): Flag name defined
            constructing the ``--no-include-line-number`` option using the
            method :py:meth:`argparse.ArgumentParser.add_argument`.
        no_include_line_number_kwargs (dict): Optional kwargs which override
            default kwargs passed to
            :py:meth:`argparse.ArgumentParser.add_argument` building the
            ``--no-include-line-number`` option.
        no_include_word (bool): Include the option
            ``--no-include-word`` which when passed in a CLI, the words
            in which mispelling errors are found are not shown in the output.
        no_include_word_name_or_flags (list): Flag name defined
            constructing the ``--no-include-word`` option using the
            method :py:meth:`argparse.ArgumentParser.add_argument`.
        no_include_word_kwargs (dict): Optional kwargs which override
            default kwargs passed to
            :py:meth:`argparse.ArgumentParser.add_argument` building the
            ``--no-include-word`` option.
        no_include_word_line_index (bool): Include the option
            ``--no-include-word-line-index`` which when passed in a CLI, the
            index of the mispelled words inside their lines in which mispelling
            errors are found are not shown in the output.
        no_include_word_line_index_name_or_flags (list): Flag name defined
            constructing the ``--no-include-word-line-index`` option using the
            method :py:meth:`argparse.ArgumentParser.add_argument`.
        no_include_word_line_index_kwargs (dict): Optional kwargs which
            override default kwargs passed to
            :py:meth:`argparse.ArgumentParser.add_argument` building the
            ``--no-include-word-line-index`` option.
        include_line (bool): Include the option ``--include-line`` which when
            passed in a CLI, the line of the mispelled words in which
            mispelling errors are found are shown in the output.
        include_line_name_or_flags (list): Flag name defined constructing the
            ``--include-line`` option using the method
            :py:meth:`argparse.ArgumentParser.add_argument`.
        include_line_kwargs (dict): Optional kwargs which override default
            kwargs passed to :py:meth:`argparse.ArgumentParser.add_argument`
            building the ``--include-line`` option.
        include_text (bool): Include the option ``--include-text`` which when
            passed in a CLI, the text in which reside found mispelled words
            is shown in the output.
        include_text_name_or_flags (list): Flag name defined constructing the
            ``--include-text`` option using the method
            :py:meth:`argparse.ArgumentParser.add_argument`.
        include_text_kwargs (dict): Optional kwargs which override default
            kwargs passed to :py:meth:`argparse.ArgumentParser.add_argument`
            building the ``--include-text`` option.
        include_error_number (bool): Include the option
            ``--include-error-number`` which when passed in a CLI, the number
            of each error is shown in the output.
        include_error_number_name_or_flags (list): Flag name defined building
            the ``--include-error-number`` option using the method
            :py:meth:`argparse.ArgumentParser.add_argument`.
        include_error_number_kwargs (dict): Optional kwargs which override
            default kwargs passed to
            :py:meth:`argparse.ArgumentParser.add_argument` building the
            ``--include-error-number`` option.
        include_near_misses (bool): Include the option
            ``--include-near-misses`` which when passed in a CLI, some Hunspell
            suggestions will be shown for each mispelled word in the report.
        include_near_misses_name_or_flags (list): Flag name defined building
            the ``--include-near-misses`` option using the method
            :py:meth:`argparse.ArgumentParser.add_argument`.
        include_near_misses_kwargs (dict): Optional kwargs which override
            default kwargs passed to
            :py:meth:`argparse.ArgumentParser.add_argument` building the
            ``--include-near-misses`` option.

    Examples:

        >>> import argparse
        >>>
        >>> parser = argparse.ArgumentParser()
        >>> hunspellchecker_argument_parser(
        ...     version=True,
        ...     version_number="1.0.0",
        ... )
        >>> opts = parser.parse_args(["--language", "es"])
        >>> print(opts)
        Namespace(languages=["es_ES"])

    """
    if version:
        version_string = render_version_template(
            version_template,
            version_template_context,
            version_prog=version_prog if version_prog is not None else parser.prog,
            version_number=version_number,
            hunspell_version=hunspell_version,
            ispell_version=ispell_version,
        )

        if version_string:
            _version_kwargs = {"action": "version", "version": version_string}
            _version_kwargs.update(version_kwargs)

            if isinstance(version_name_or_flags, str):  # pragma: no cover
                version_name_or_flags = [version_name_or_flags]

            parser.add_argument(*version_name_or_flags, **_version_kwargs)
        else:
            readable_version_option = "/".join(version_name_or_flags)
            warnings.warn(
                f"'{readable_version_option}' option not added because version"
                " string is empty!"
            )

    if files:
        _files_kwargs = {
            "nargs": "*",
            "type": str,
            "dest": "files",
            "metavar": "FILES",
            "help": "Files and/or globs to check.",
            "action": FilesOrGlobsAction,
        }
        _files_kwargs.update(files_kwargs)
        parser.add_argument(**_files_kwargs)

    if languages:
        _languages_kwargs = {
            "type": str,
            "required": True,
            "metavar": "LANGUAGE",
            "dest": "languages",
            "help": "Language to check, you'll have to install the"
            " corresponding hunspell dictionary.",
        }

        _languages_kwargs["action"] = create_hunspell_valid_dictionary_action(
            negotiate_languages=negotiate_languages,
        )
        _languages_kwargs.update(languages_kwargs)

        if isinstance(languages_name_or_flags, str):  # pragma: no cover
            languages_name_or_flags = [languages_name_or_flags]

        parser.add_argument(*languages_name_or_flags, **_languages_kwargs)

    if personal_dicts:
        _personal_dicts_kwargs = {
            "type": str,
            "required": False,
            "metavar": "PERSONAL_DICTIONARY",
            "dest": "personal_dicts",
            "help": "Additional dictionaries to extend the words to exclude.",
            "action": PersonalDictionaryAction,
            "nargs": 1,
            "default": None,
        }
        _personal_dicts_kwargs.update(personal_dicts_kwargs)

        if isinstance(personal_dicts_name_or_flags, str):  # pragma: no cover
            personal_dicts_name_or_flags = [personal_dicts_name_or_flags]

        parser.add_argument(*personal_dicts_name_or_flags, **_personal_dicts_kwargs)

    if encoding:
        _encoding_kwargs = {
            "type": str,
            "required": False,
            "metavar": "ENCODING",
            "dest": "encoding",
            "help": "Input content encoding.",
            "action": "store",
            "default": None,
        }
        _encoding_kwargs.update(encoding_kwargs)

        if isinstance(encoding_name_or_flags, str):  # pragma: no cover
            encoding_name_or_flags = [encoding_name_or_flags]

        parser.add_argument(*encoding_name_or_flags, **_encoding_kwargs)

    if digits_are_words:
        _digits_are_words_kwargs = {
            "action": "store_true",
            "required": False,
            "dest": "digits_are_words",
            "default": False,
            "help": (
                "Words compound only by digits will be considered words and"
                " will be checked for possible mispelling errors."
            ),
        }
        _digits_are_words_kwargs.update(digits_are_words_kwargs)

        if isinstance(digits_are_words_name_or_flags, str):  # pragma: no cover
            digits_are_words_name_or_flags = [digits_are_words_name_or_flags]

        parser.add_argument(*digits_are_words_name_or_flags, **_digits_are_words_kwargs)

    if words_not_contain_digits:
        _words_not_contain_digits_kwargs = {
            "action": "store_false",
            "required": False,
            "dest": "words_can_contain_digits",
            "default": True,
            "help": (
                "Words that contain a digit inside will not be considered words"
                " and will be ignored checking possible mispelling errors."
            ),
        }
        _words_not_contain_digits_kwargs.update(words_not_contain_digits_kwargs)

        if isinstance(words_not_contain_digits_name_or_flags, str):  # pragma: no cover
            words_not_contain_digits_name_or_flags = [
                words_not_contain_digits_name_or_flags
            ]

        parser.add_argument(
            *words_not_contain_digits_name_or_flags, **_words_not_contain_digits_kwargs
        )

    if words_not_startswith_dash:
        _words_not_startswith_dash_kwargs = {
            "action": "store_false",
            "required": False,
            "dest": "words_can_startswith_dash",
            "default": True,
            "help": (
                "Words starting with the character '-' will not be checked for"
                " possible mispelling errors."
            ),
        }
        _words_not_startswith_dash_kwargs.update(words_not_startswith_dash_kwargs)

        if isinstance(words_not_startswith_dash_name_or_flags, str):  # pragma: no cover
            words_not_startswith_dash_name_or_flags = [
                words_not_startswith_dash_name_or_flags
            ]

        parser.add_argument(
            *words_not_startswith_dash_name_or_flags,
            **_words_not_startswith_dash_kwargs,
        )

    if words_not_endswith_dash:
        _words_not_endswith_dash_kwargs = {
            "action": "store_false",
            "required": False,
            "dest": "words_can_endswith_dash",
            "default": True,
            "help": (
                "Words ending with the character '-' will not be checked for"
                " possible mispelling errors."
            ),
        }
        _words_not_endswith_dash_kwargs.update(words_not_endswith_dash_kwargs)

        if isinstance(words_not_endswith_dash_name_or_flags, str):  # pragma: no cover
            words_not_endswith_dash_name_or_flags = [
                words_not_endswith_dash_name_or_flags
            ]

        parser.add_argument(
            *words_not_endswith_dash_name_or_flags, **_words_not_endswith_dash_kwargs
        )

    if words_not_contain_dash:
        _words_not_contain_dash_kwargs = {
            "action": "store_false",
            "required": False,
            "dest": "words_can_contain_dash",
            "default": True,
            "help": (
                "Words containing the character '-' will not be checked for"
                " possible mispelling errors."
            ),
        }
        _words_not_contain_dash_kwargs.update(words_not_contain_dash_kwargs)

        if isinstance(words_not_contain_dash_name_or_flags, str):  # pragma: no cover
            words_not_contain_dash_name_or_flags = [
                words_not_contain_dash_name_or_flags
            ]

        parser.add_argument(
            *words_not_contain_dash_name_or_flags, **_words_not_contain_dash_kwargs
        )

    if words_not_contain_two_upper:
        _words_not_contain_two_upper_kwargs = {
            "action": "store_false",
            "required": False,
            "dest": "words_can_contain_two_upper",
            "default": True,
            "help": (
                "Words containing two or more uppercase letters will not be"
                " checked for possible mispelling errors."
            ),
        }
        _words_not_contain_two_upper_kwargs.update(words_not_contain_two_upper_kwargs)

        if isinstance(
            words_not_contain_two_upper_name_or_flags, str
        ):  # pragma: no cover
            words_not_contain_two_upper_name_or_flags = [
                words_not_contain_two_upper_name_or_flags
            ]

        parser.add_argument(
            *words_not_contain_two_upper_name_or_flags,
            **_words_not_contain_two_upper_kwargs,
        )

    if no_include_filename:
        _no_include_filename_kwargs = {
            "action": "store_false",
            "required": False,
            "dest": "include_filename",
            "default": True,
            "help": "Filenames will not be included in spellchecking errors report.",
        }
        _no_include_filename_kwargs.update(no_include_filename_kwargs)

        if isinstance(no_include_filename_name_or_flags, str):  # pragma: no cover
            no_include_filename_name_or_flags = [no_include_filename_name_or_flags]

        parser.add_argument(
            *no_include_filename_name_or_flags, **_no_include_filename_kwargs
        )

    if no_include_line_number:
        _no_include_line_number_kwargs = {
            "action": "store_false",
            "required": False,
            "dest": "include_line_number",
            "default": True,
            "help": "Line numbers will not be included in spellchecking errors report.",
        }
        _no_include_line_number_kwargs.update(no_include_line_number_kwargs)

        if isinstance(no_include_line_number_name_or_flags, str):  # pragma: no cover
            no_include_line_number_name_or_flags = [
                no_include_line_number_name_or_flags
            ]

        parser.add_argument(
            *no_include_line_number_name_or_flags, **_no_include_line_number_kwargs
        )

    if no_include_word:
        _no_include_word_kwargs = {
            "action": "store_false",
            "required": False,
            "dest": "include_word",
            "default": True,
            "help": "Words will not be included in spellchecking errors report.",
        }
        _no_include_word_kwargs.update(no_include_word_kwargs)

        if isinstance(no_include_word_name_or_flags, str):  # pragma: no cover
            no_include_word_name_or_flags = [no_include_word_name_or_flags]

        parser.add_argument(*no_include_word_name_or_flags, **_no_include_word_kwargs)

    if no_include_word_line_index:
        _no_include_word_line_index_kwargs = {
            "action": "store_false",
            "required": False,
            "dest": "include_word_line_index",
            "default": True,
            "help": (
                "Index of mispelled words inside their lines will not be"
                " included in spellchecking errors report."
            ),
        }
        _no_include_word_line_index_kwargs.update(no_include_word_line_index_kwargs)

        if isinstance(
            no_include_word_line_index_name_or_flags, str
        ):  # pragma: no cover
            no_include_word_line_index_name_or_flags = [
                no_include_word_line_index_name_or_flags
            ]

        parser.add_argument(
            *no_include_word_line_index_name_or_flags,
            **_no_include_word_line_index_kwargs,
        )

    if include_line:
        _include_line_kwargs = {
            "action": "store_true",
            "required": False,
            "dest": "include_line",
            "default": False,
            "help": (
                "Entire lines inside mispelled words are found will be shown in"
                " the report."
            ),
        }
        _include_line_kwargs.update(include_line_kwargs)

        if isinstance(include_line_name_or_flags, str):  # pragma: no cover
            include_line_name_or_flags = [include_line_name_or_flags]

        parser.add_argument(*include_line_name_or_flags, **_include_line_kwargs)

    if include_text:
        _include_text_kwargs = {
            "action": "store_true",
            "required": False,
            "dest": "include_text",
            "default": False,
            "help": (
                "Entire texts inside mispelled words are found will be shown"
                " in the report."
            ),
        }
        _include_text_kwargs.update(include_text_kwargs)

        if isinstance(include_text_name_or_flags, str):  # pragma: no cover
            include_text_name_or_flags = [include_text_name_or_flags]

        parser.add_argument(*include_text_name_or_flags, **_include_text_kwargs)

    if include_error_number:
        _include_error_number_kwargs = {
            "action": "store_true",
            "required": False,
            "dest": "include_error_number",
            "default": False,
            "help": ("A counter for each mispelled word will be shown in the report."),
        }
        _include_error_number_kwargs.update(include_error_number_kwargs)

        if isinstance(include_error_number_name_or_flags, str):  # pragma: no cover
            include_error_number_name_or_flags = [include_error_number_name_or_flags]

        parser.add_argument(
            *include_error_number_name_or_flags, **_include_error_number_kwargs
        )

    if include_near_misses:
        _include_near_misses_kwargs = {
            "action": "store_true",
            "required": False,
            "dest": "include_near_misses",
            "default": False,
            "help": (
                "Some Hunspell suggestions for each mispelled word will be"
                " shown in the report."
            ),
        }
        _include_near_misses_kwargs.update(include_near_misses_kwargs)

        if isinstance(include_near_misses_name_or_flags, str):  # pragma: no cover
            include_near_misses_name_or_flags = [include_near_misses_name_or_flags]

        parser.add_argument(
            *include_near_misses_name_or_flags, **_include_near_misses_kwargs
        )
