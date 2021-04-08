# hunspellcheck

[![PyPI][pypi-version-badge-link]][pypi-link]
[![Python versions][pypi-pyversions-badge-link]][pypi-link]
[![License][license-image]][license-link]
[![Tests][tests-image]][tests-link]

This library is a helper for writing spell checkers using hunspell.

If you want to standarize the execution and writing of several spell checkers
for different file types, performing the spell checking against ortographic
dictionaries, this library is for you. It will allow you to reuse some patterns
repeated using hunspell for spell checking.

## Features

- Graceful handling of missing dictionaries.
- Custom dictionaries by filepath.
- Personal dictionaries by filepath.
- Argument parsers building.
- Well tested system calls to `hunspell`.

## Install

```bash
pip install hunspellcheck
```

## Example

Let's write a `.txt` files spellchecker. It's really easy:

### CLI interface

```python
"""__main__.py"""

import argparse
import sys

from hunspellcheck import (
    extend_argument_parser,
    render_error,
    SpellChecker,
)


def build_parser():
    parser = argparse.ArgumentParser(description="TXT files spellchecker.")
    extend_argument_parser(
        parser,
        version=True,
        version_number="1.0.0",
    )
    return parser


def main():
    opts = build_parser().parse_args()
    
    # Is your mission to extract the contents of the files.
    # By default are passed as globs in positional arguments and stored in
    # the 'files' property of the namespace
    filenames_contents = {}
    for filename in opts.files:
        with open(filename, "r") as f:
            filenames_contents[filename] = f.read()
    
    spellchecker = SpellChecker(
        filenames_contents=filenames_contents,
        languages=opts.languages,
        personal_dict=opts.personal_dict,
    )
    for error in spellchecker.check():
        print(render_error(error), file=sys.stderr)

    return 0 if not spellchecker.errors else 1


if __name__ == "__main__":
    sys.exit(main())
```

You can see the usage passing `--help` to this script:

```bash
$ python3 __main__.py --help
usage: __main__.py [-h] [--version] -l LANGUAGE [-p PERSONAL_DICTIONARY] [FILES [FILES ...]]

positional arguments:
  FILES                 Files and/or globs to check.

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -l LANGUAGE, --languages LANGUAGE
                        Language to check, you'll have to install the corresponding hunspell dictionary.
  -p PERSONAL_DICTIONARY, --personal-dict PERSONAL_DICTIONARY
                        Additional dictionary to extend the words to exclude.
```

To use it, just create a `.txt` file and pass its filename as positional
argument, selecting the language with `--language` option:

```txt
Texto en español y word
```

```bash
$ python3 __main__.py --language es_ES foo.txt
foo.txt:word:1:19
```

[pypi-link]: https://pypi.org/project/hunspellcheck
[pypi-version-badge-link]: https://img.shields.io/pypi/v/hunspellcheck
[pypi-pyversions-badge-link]: https://img.shields.io/pypi/pyversions/hunspellcheck
[license-image]: https://img.shields.io/pypi/l/hunspellcheck?color=light-green
[license-link]: https://github.com/mondeja/hunspellcheck/blob/master/LICENSE
[tests-image]: https://img.shields.io/github/workflow/status/mondeja/hunspellcheck/CI
[tests-link]: https://github.com/mondeja/hunspellcheck/actions?query=workflow%3ACI
