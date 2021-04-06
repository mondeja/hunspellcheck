"""Hunspell related functions."""

import os
import subprocess
import sys


def gen_available_dictionaries():
    """Generates the available dictionaries contained inside the search paths
    configured by hunspell.

    These dictionaries can be used without specify the full path to their
    location in the system calling hunspell, only their name is needed.
    """
    # TODO: Windows support -> https://stackoverflow.com/a/62117664/9167585
    previous_env_lang = os.environ.get("LANG", "")
    os.environ["LANG"] = "C"

    command = [
        "hunspell",
        "-D",
    ]
    output = subprocess.run(command, stderr=subprocess.PIPE)

    os.environ["LANG"] = previous_env_lang

    _inside_available_dictionaries = False
    for line in output.stderr.decode("utf-8").splitlines():
        if _inside_available_dictionaries:
            yield os.path.basename(line)
        elif line.startswith("AVAILABLE DICTIONARIES"):
            _inside_available_dictionaries = True


def list_available_dictionaries():
    """Convenient wrapper around the generator
    :py:func:`hunspell_checker.hunspell.gen_available_dictionaries` that
    returns the dictionary names in a list."""
    return list(gen_available_dictionaries())


def print_available_dictionaries(sort=True, stream=sys.stdout):
    """Prints into an stream the available hunspell dictionaries.

    By default are printed to the standard output of the system (STDOUT).

    Args:
        sort (bool): Indicates if the dictionaries will be printed in
            alphabetical order.
        stream (object): Stream to which the dictionaries will be printed.
            Must be any object that accepts a `write` method.
    """
    if sort:
        dictionaries_iter = sorted(list_available_dictionaries())
    else:
        dictionaries_iter = gen_available_dictionaries()

    for dictname in dictionaries_iter:
        stream.write(f"{dictname}\n")
