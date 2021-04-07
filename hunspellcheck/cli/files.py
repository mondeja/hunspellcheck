"""Files positional argument related stuff for hunspellcheck CLI utilities."""

import argparse
import glob


class FilesOrGlobsAction(argparse._ExtendAction):
    def __call__(self, parser, namespace, values, option_string=None):
        filenames = []
        for value in values:
            filenames.extend(glob.glob(value))
        super().__call__(parser, namespace, filenames, option_string=option_string)
