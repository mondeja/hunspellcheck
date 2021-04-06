# hunspellcheck

[![PyPI][pypi-version-badge-link]][pypi-link]
[![Python versions][pypi-pyversions-badge-link]][pypi-link]
[![License][license-image]][license-link]
[![Tests][tests-image]][tests-link]

This library is a helper for writing spell checkers using hunspell.

If you want to standarize the execution and writing of several spell checkers
for different kind of file types, performing the spell checking against
ortographic dictionaries, this library is for you. It will allow you to reuse
some patterns repeated using hunspell:

- Argument parsers building.
- System calls to hunspell.
- Define a set of callbacks in the spell checking process.

## Install

```bash
pip install hunspellcheck
```

## Documentation




[pypi-link]: https://pypi.org/project/hunspellcheck
[pypi-version-badge-link]: https://img.shields.io/pypi/v/hunspellcheck
[pypi-pyversions-badge-link]: https://img.shields.io/pypi/pyversions/hunspellcheck
[license-image]: https://img.shields.io/pypi/l/hunspellcheck?color=light-green
[license-link]: https://github.com/mondeja/hunspellcheck/blob/master/LICENSE
[tests-image]: https://img.shields.io/github/workflow/status/mondeja/hunspellcheck/CI
[tests-link]: https://github.com/mondeja/hunspellcheck/actions?query=workflow%3ACI
