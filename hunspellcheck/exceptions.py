"""Exceptons module of hunspellcheck."""


class HunspellCheckException(Exception):
    """All exceptions from this module inherit from this one."""


class Unreachable(HunspellCheckException):
    """The code encontered a state that should be unreachable."""
