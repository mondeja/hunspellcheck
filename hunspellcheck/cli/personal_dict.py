"""Personal dictionary CLI option stuff."""

import argparse
import os


class PersonalDictionaryAction(argparse._StoreAction):
    def __call__(self, parser, namespace, values, option_string=None):
        if not os.path.isfile(values[0]):
            raise FileNotFoundError(
                f"Personal dictionary file not found at \"{values}\""
            )
        super().__call__(parser, namespace, values[0], option_string=option_string)
