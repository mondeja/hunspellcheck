"""Test a TXT spellchecker implementation."""

import argparse
import contextlib
import glob
import io
import os
import re
import sys
import tempfile

import pytest

from hunspellcheck import (
    HunspellChecker,
    assert_is_valid_dictionary_language_or_filename,
    hunspellchecker_argument_parser,
    looks_like_a_word_creator,
    render_hunspell_word_error,
)


class HunspellCheckerInterfaceUtil:
    def _create_temp_file(self, content):
        filename = tempfile.NamedTemporaryFile().name
        if os.path.isfile(filename):
            os.remove(filename)

        with open(filename, "w") as f:
            f.write(content)
        return filename


class TestHunspellCheckerTxtCLI(HunspellCheckerInterfaceUtil):
    def build_parser(self):
        parser = argparse.ArgumentParser()
        hunspellchecker_argument_parser(
            parser,
            version=True,
            version_number="1.0.0",
        )
        return parser

    def main(self, args):
        opts = self.build_parser().parse_args(args)

        filenames_contents = {}
        for filename in opts.files:
            with open(filename) as f:
                filenames_contents[filename] = f.read()

        spellchecker = HunspellChecker(
            filenames_contents=filenames_contents,
            languages=opts.languages,
            personal_dicts=opts.personal_dicts,
            encoding=opts.encoding,
            looks_like_a_word=looks_like_a_word_creator(
                digits_are_words=opts.digits_are_words,
                words_can_contain_digits=opts.words_can_contain_digits,
                words_can_startswith_dash=opts.words_can_startswith_dash,
                words_can_endswith_dash=opts.words_can_endswith_dash,
                words_can_contain_dash=opts.words_can_contain_dash,
            ),
        )
        for word_error in spellchecker.check():
            sys.stderr.write(f"{render_hunspell_word_error(word_error)}\n")

        return 0 if not spellchecker.errors else 1

    def test_version(self):
        # test '--version'
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), pytest.raises(SystemExit):
            self.main(["--version"])
        assert re.match(
            (
                rf"^{os.path.basename(sys.argv[0])} 1\.0\.0 - Hunspell"
                r" \d+\.\d+\.\d+ - Ispell \d+\.\d+\.\d+"
            ),
            stdout.getvalue(),
        )

    def test_error_found(self):
        filename = self._create_temp_file(
            "Algo de texto en español y ahora en english\n"
        )

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            returncode = self.main(["-l", "es_ES", filename])

        assert stderr.getvalue() == f"{filename}:english:1:36\n"
        assert returncode == 1

    def test_language_required(self):
        filename = self._create_temp_file("")

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), pytest.raises(SystemExit):
            self.main([filename])
        assert "error: the following arguments are required: -l/--language" in (
            stderr.getvalue()
        )


class TestHunspellCheckerTxtAPI(HunspellCheckerInterfaceUtil):
    def txt_file_to_content(self, filename, encoding=None):
        with open(filename, encoding=encoding) as f:
            return f.read()

    def main(
        self,
        files,
        languages,
        personal_dicts=None,
        negotiate_languages=False,
        encoding=None,
        include_filename=True,
        include_line_number=True,
        include_word=True,
        include_word_line_index=True,
        include_line=False,
        include_text=False,
        include_error_number=False,
        include_near_misses=False,
        digits_are_words=False,
        words_can_contain_digits=True,
        words_can_startswith_dash=True,
        words_can_endswith_dash=True,
        words_can_contain_dash=True,
    ):
        assert_is_valid_dictionary_language_or_filename(
            languages,
            negotiate_languages=negotiate_languages,
        )

        filename_contents = {}
        for glob_files in files:
            for filename in glob.glob(glob_files):
                filename_contents[filename] = self.txt_file_to_content(
                    filename,
                    encoding=encoding,
                )

        yield from HunspellChecker(
            filename_contents,
            languages,
            personal_dicts=personal_dicts,
            looks_like_a_word=looks_like_a_word_creator(
                digits_are_words=digits_are_words,
                words_can_contain_digits=words_can_contain_digits,
                words_can_startswith_dash=words_can_startswith_dash,
                words_can_endswith_dash=words_can_endswith_dash,
                words_can_contain_dash=words_can_contain_dash,
            ),
            encoding=encoding,
        ).check(
            include_filename=include_filename,
            include_line_number=include_line_number,
            include_word=include_word,
            include_word_line_index=include_word_line_index,
            include_line=include_line,
            include_text=include_text,
            include_error_number=include_error_number,
            include_near_misses=include_near_misses,
        )

    @pytest.mark.parametrize(
        "languages", ("es_ES", ["es_ES"]), ids=("es_ES", "[es_ES]")
    )
    def test_error_found(self, languages):
        filename = self._create_temp_file("Algo de texto en español y ahora en english")

        n_errors = 0
        for word_error in self.main([filename], languages):
            assert word_error["word"] == "english"
            assert word_error["filename"] == filename
            assert word_error["line_number"] == 1
            assert word_error["word_line_index"] == 36
            n_errors += 1

        assert n_errors == 1
