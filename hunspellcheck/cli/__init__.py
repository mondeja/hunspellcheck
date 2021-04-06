"""CLI utilities writing spell checkers."""

from hunspellcheck.cli.language import HunspellDictionaryNegotiatorAction
from hunspellcheck.cli.personal_dict import PersonalDictionaryAction


def extend_argument_parser(
    parser,
    language=True,
    language_args=["-l", "--language"],
    language_kwargs={},
    negotiate_language=True,
    personal_dict=True,
    personal_dict_args=["-p", "--personal-dict"],
    personal_dict_kwargs={},
):
    if language:
        _language_kwargs = {
            "type": str,
            "required": True,
            "metavar": "LANGUAGE",
            "dest": "language",
            "help": "Language to check, you'll have to install the"
                    " corresponding hunspell dictionary."
        }

        if negotiate_language:
            _language_kwargs["action"] = HunspellDictionaryNegotiatorAction
        else:
            _language_kwargs["action"] = "extend"

        _language_kwargs.update(language_kwargs)

        parser.add_argument(*language_args, **_language_kwargs)

    if personal_dict:
        _personal_dict_kwargs = {
            "type": str,
            "required": False,
            "metavar": "PERSONAL_DICTIONARY",
            "dest": "personal_dict",
            "help": "Additional dictionary to extend the words to exclude.",
            "action": PersonalDictionaryAction,
            "nargs": 1,
            "default": None,
        }
        _personal_dict_kwargs.update(personal_dict_kwargs)
        parser.add_argument(*personal_dict_args, **_personal_dict_kwargs)
