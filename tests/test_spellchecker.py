"""Hunspellcheck spellchecker tests."""

import os
import tempfile

import pytest

from hunspellcheck import HunspellChecker


class TestHunspellChecker:
    @pytest.mark.parametrize(
        (
            "filenames_contents",
            "language_dicts",
            "include_filename",
            "include_line_number",
            "include_word",
            "include_word_line_index",
            "include_line",
            "include_text",
            "include_error_number",
            "include_near_misses",
            "expected_errors",
        ),
        (
            (
                {"foo.txt": ""},
                "es_ES",
                True,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                [],
            ),
            (
                {"foo.txt": "tr\n"},
                "es_ES",
                True,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                [{"filename": "foo.txt"}],
            ),
            (
                {"foo.txt": "tr td\n"},
                "es_ES",
                True,
                True,
                False,
                False,
                False,
                False,
                False,
                False,
                [
                    {
                        "filename": "foo.txt",
                        "line_number": 1,
                    },
                    {
                        "filename": "foo.txt",
                        "line_number": 1,
                    },
                ],
            ),
            (
                {"foo.txt": "hola hoal hiuli\niuyh"},
                "es_ES",
                True,
                True,
                True,
                False,
                False,
                False,
                False,
                False,
                [
                    {
                        "filename": "foo.txt",
                        "line_number": 1,
                        "word": "hoal",
                    },
                    {
                        "filename": "foo.txt",
                        "line_number": 1,
                        "word": "hiuli",
                    },
                    {
                        "filename": "foo.txt",
                        "line_number": 2,
                        "word": "iuyh",
                    },
                ],
            ),
            (
                {"foo.txt": "aliy\n  eufh"},
                "es_ES",
                True,
                True,
                True,
                True,
                False,
                False,
                False,
                False,
                [
                    {
                        "filename": "foo.txt",
                        "line_number": 1,
                        "word": "aliy",
                        "word_line_index": 0,
                    },
                    {
                        "filename": "foo.txt",
                        "line_number": 2,
                        "word": "eufh",
                        "word_line_index": 2,
                    },
                ],
            ),
            (
                {"foo.txt": " uhfy"},
                "es_ES",
                True,
                True,
                True,
                True,
                True,
                False,
                False,
                False,
                [
                    {
                        "filename": "foo.txt",
                        "line_number": 1,
                        "word": "uhfy",
                        "word_line_index": 1,
                        "line": " uhfy",
                    }
                ],
            ),
            (
                {
                    "foo.txt": "ahui ejemplo",
                    "bar.txt": " urtk\nentonces",
                },
                "es_ES",
                True,
                True,
                True,
                True,
                True,
                True,
                False,
                False,
                [
                    {
                        "filename": "foo.txt",
                        "line_number": 1,
                        "word": "ahui",
                        "word_line_index": 0,
                        "line": "ahui ejemplo",
                        "text": "ahui ejemplo",
                    },
                    {
                        "filename": "bar.txt",
                        "line_number": 1,
                        "word": "urtk",
                        "word_line_index": 1,
                        "line": " urtk",
                        "text": " urtk\nentonces",
                    },
                ],
            ),
            (
                {"foo.txt": "bar baz"},
                "es_ES",
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                False,
                [
                    {
                        "filename": "foo.txt",
                        "line_number": 1,
                        "word": "baz",
                        "word_line_index": 4,
                        "line": "bar baz",
                        "text": "bar baz",
                        "error_number": 1,
                    }
                ],
            ),
            (
                {"foo.txt": "near"},
                "es_ES",
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                [
                    {
                        "filename": "foo.txt",
                        "line_number": 1,
                        "word": "near",
                        "word_line_index": 0,
                        "line": "near",
                        "text": "near",
                        "error_number": 1,
                        "near_misses": [
                            "mear",
                            "nea",
                            "anear",
                            "negar",
                            "nevar",
                            "neas",
                            "ne",
                            "ar",
                            "ne-ar",
                            "necear",
                        ],
                    }
                ],
            ),
        ),
    )
    def test_includes(
        self,
        filenames_contents,
        language_dicts,
        include_filename,
        include_line_number,
        include_word,
        include_word_line_index,
        include_line,
        include_text,
        include_error_number,
        include_near_misses,
        expected_errors,
    ):
        spellchecker = HunspellChecker(filenames_contents, language_dicts)

        error_index = 0
        for error in spellchecker.check(
            include_filename=include_filename,
            include_line_number=include_line_number,
            include_word=include_word,
            include_word_line_index=include_word_line_index,
            include_line=include_line,
            include_text=include_text,
            include_error_number=include_error_number,
            include_near_misses=include_near_misses,
        ):
            assert len(error.keys()) == len(expected_errors[error_index].keys())
            for field, value in expected_errors[error_index].items():
                assert value == error[field]
            error_index += 1
        assert spellchecker.errors == len(expected_errors)

    @pytest.mark.parametrize(
        (
            "filenames_contents",
            "language_dicts",
            "personal_dicts_contents",
            "expected_errors",
        ),
        (
            (
                {"foo.txt": "hola hoal hiul"},
                "es_ES",
                ["hoal"],
                [
                    {
                        "filename": "foo.txt",
                        "line_number": 1,
                        "word": "hiul",
                        "word_line_index": 10,
                    }
                ],
            ),
            (
                {"bar.txt": "uyih calor iuej"},
                "es_ES",
                ["uyih\niuej"],
                [],
            ),
            (
                {"foo.txt": "hola hoal iuli ythu"},
                "es_ES",
                ["hoal", "iuli"],
                [
                    {
                        "filename": "foo.txt",
                        "line_number": 1,
                        "word": "ythu",
                        "word_line_index": 15,
                    }
                ],
            ),
        ),
    )
    def test_personal_dicts(
        self,
        filenames_contents,
        language_dicts,
        personal_dicts_contents,
        expected_errors,
    ):
        personal_dicts = []
        for personal_dict_content in personal_dicts_contents:
            personal_dict_filename = tempfile.NamedTemporaryFile().name
            if os.path.isfile(personal_dict_filename):
                os.remove(personal_dict_filename)
            with open(personal_dict_filename, "w") as f:
                f.write(personal_dict_content)
            personal_dicts.append(personal_dict_filename)

        spellchecker = HunspellChecker(
            filenames_contents,
            language_dicts,
            personal_dicts=personal_dicts,
        )

        error_index = 0
        for error in spellchecker.check():
            assert len(error.keys()) == len(expected_errors[error_index].keys())
            for field, value in expected_errors[error_index].items():
                assert value == error[field]
            error_index += 1

        assert spellchecker.errors == len(expected_errors)

        for personal_dict_filename in personal_dicts:
            os.remove(personal_dict_filename)
