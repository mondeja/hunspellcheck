"""Test a TXT spellchecker implementation."""

import argparse
import contextlib
import io
import os
import re
import sys
import tempfile

import pytest

from hunspellcheck import (
    HunspellChecker,
    extend_argument_parser,
    render_hunspell_word_error,
)


class TestHunspellCheckerTxtCLI:
    def build_parser(self):
        parser = argparse.ArgumentParser()
        extend_argument_parser(
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
            personal_dict=opts.personal_dict,
        )
        for word_error in spellchecker.check():
            sys.stderr.write(f"{render_hunspell_word_error(word_error)}\n")

        return 0 if not spellchecker.errors else 1

    def _create_temp_file(self, content):
        filename = tempfile.NamedTemporaryFile().name
        if os.path.isfile(filename):
            os.remove(filename)

        with open(filename, "w") as f:
            f.write(content)
        return filename

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
            "Algo de texto en español y ahora in english\n"
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
