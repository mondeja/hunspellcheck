"""Language option related stuff for hunspellcheck CLI utilities."""

import argparse
import os

from babel import Locale

from hunspellcheck.hunspell.dictionaries import (
    gen_available_dictionaries_with_langcodes,
    list_available_dictionaries,
)


class HunspellDictionaryNegotiatorAction(argparse._AppendAction):
    """This action allows to redirect a language like 'es' or a dictionary
    filepath to a valid language dictionary supported by hunspell.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        if os.path.isfile(values):
            values = values.rstrip(".dic").rstrip(".aff")
        else:
            available_dictionaries = list_available_dictionaries()
            if values not in available_dictionaries:
                values = str(Locale.negotiate([values], available_dictionaries))
            self.choices = list(gen_available_dictionaries_with_langcodes())
            self.choices.append("<dictionary filepath>")

        # check value manually (seems to me like a hack, but it works)
        parser._check_value(self, values)
        super().__call__(parser, namespace, values, option_string=option_string)
