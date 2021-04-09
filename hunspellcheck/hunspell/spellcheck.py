"""Spell checking system calls to Hunspell."""

import subprocess


def hunspell_spellcheck(
    content,
    language_dicts,
    personal_dict=None,
    encoding=None,
):
    """Call hunspell for spellchecing.

    Args:
        content (str): Content to check for words not included in dictionaries.
        language_dicts (list, str): Language or languages dictionaries (could
            be defined as files) used to check errors.
        personal_dict (str): Personal dictionary used to exclude valid words
            from being notified as errors.
        encoding (str): Input encoding passed to Hunspell. If is defined, the
            option ``-i`` will be passed to hunspell system call.

    Returns:
        str: Hunspell standard output.
    """
    if not isinstance(language_dicts, str):
        language_dicts = ",".join(language_dicts)

    command = ["hunspell", "-d", language_dicts, "-a"]
    if personal_dict:
        command.extend(["-p", personal_dict])
    if encoding:
        command.extend(["-i"], encoding)

    return subprocess.run(
        command,
        universal_newlines=True,
        input=content,
        stdout=subprocess.PIPE,
        check=True,
    )
