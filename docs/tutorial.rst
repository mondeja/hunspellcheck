********
Tutorial
********

Basic ``.txt`` files spellchecker
=================================

Command line interface
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   """__main__.py"""

   import argparse
   import sys

   from hunspellcheck import (
       extend_argument_parser,
       render_hunspell_word_error,
       HunspellChecker,
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

       spellchecker = HunspellChecker(
           filenames_contents=filenames_contents,
           languages=opts.languages,
           personal_dict=opts.personal_dict,
       )
       for word_error in spellchecker.check():
           print(render_hunspell_word_error(word_error), file=sys.stderr)

       return 0 if not spellchecker.errors else 1


   if __name__ == "__main__":
       sys.exit(main())


You can see the usage passing ``--help`` option to this script:

.. code-block::

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


To use it, just create a ``.txt`` file and pass its filename as positional
argument, selecting the language with ``--language`` option:

.. code-block::

   Texto en español y word


.. code-block:: bash

   $ python3 __main__.py --language es_ES foo.txt
   foo.txt:word:1:19


Public API interface
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   """__init__.py"""

   from hunspellcheck import (
      HunspellChecker,
      assert_is_valid_dictionary_language_or_filename,
      looks_like_a_word,
   )

   def txt_spell(
        self,
        filename_contents,
        languages,
        personal_dict=None,
        negotiate_languages=False,
        include_filename=True,
        include_line_number=True,
        include_word=True,
        include_word_line_index=True,
        include_line=False,
        include_text=False,
        include_error_number=False,
        include_near_misses=False,
        looks_like_a_word=looks_like_a_word,
   ):
        assert_is_valid_dictionary_language_or_filename(
            languages,
            negotiate_languages=negotiate_languages,
        )

        yield from HunspellChecker(
            filename_contents,
            languages,
            personal_dict=personal_dict,
            looks_like_a_word=looks_like_a_word,
        ).check(
            include_filename=include_filename,
            include_line_number=include_line_number,
            include_word=include_word,
            include_word_line_index=include_word_line_index,
            include_line=include_line,
            include_text=include_text,
            include_error_number=include_error_number,
            include_near_misses=include_near_misses,
        )


The function will yield from a generator:

.. code-block:: python

   for word_error in txt_spell({"foo.txt": "hello hola"}, "es_ES"):
       print(word_error)

.. code-block:: python

   {'filename': 'foo.txt', 'line_number': 1, 'word': 'hello', 'word_line_index': 0}
