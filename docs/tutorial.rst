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
       hunspellchecker_argument_parser,
       render_hunspell_word_error,
       HunspellChecker,
   )


   def build_parser():
       parser = argparse.ArgumentParser(description="TXT files spellchecker.")
       hunspellchecker_argument_parser(
           parser,
           version=True,
           version_number="1.0.0",
       )
       return parser


   def main():
       opts = build_parser().parse_args()

       # Extracting content from the files is the task you must focused in.
       # By default are passed as globs in positional arguments and stored in
       # the 'files' property of the namespace
       filenames_contents = {}
       for filename in opts.files:
           with open(filename, "r") as f:
               filenames_contents[filename] = f.read()

       spellchecker = HunspellChecker(
           filenames_contents=filenames_contents,
           languages=opts.languages,
           personal_dicts=opts.personal_dicts,
           encoding=opts.encoding,
           looks_like_a_word=looks_like_a_word_creator(
               digits_are_words=opts.digits_are_words,
               words_can_contain_digits=opts.words_can_contain_digits,
               words_can_startswith_dash=opts.words_can_startswith_dash,
               words_can_endswith_dash=opts.words_can_endswith_dash,
               words_can_contain_dash=opts.words_can_contain_dash,
           ),
       )
       for word_error in spellchecker.check():
           print(render_hunspell_word_error(word_error), file=sys.stderr)

       return 0 if not spellchecker.errors else 1


   if __name__ == "__main__":
       sys.exit(main())


You can see the usage passing ``--help`` option to this script.

To use it, just create a ``.txt`` file and pass its filename as positional
argument, selecting the language with ``--language`` option:

.. code-block::

   hola hello

.. code-block:: bash

   $ python3 __main__.py --language es_ES foo.txt
   foo.txt:hello:1:5


Public API interface
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   """__init__.py"""

   import glob

   from hunspellcheck import (
      HunspellChecker,
      assert_is_valid_dictionary_language_or_filename,
      looks_like_a_word_creator,
   )

   def txt_file_to_content(filename, encoding=None):
       with open(filename, "r", encoding=encoding) as f:
           return f.read()

   def txt_spell(
        self,
        files,
        languages,
        personal_dicts=None,
        negotiate_languages=False,
        encoding=None,
        include_filename=True,
        include_line_number=True,
        include_word=True,
        include_word_line_index=True,
        include_line=False,
        include_text=False,
        include_error_number=False,
        include_near_misses=False,
        digits_are_words=False,
        words_can_contain_digits=True,
        words_can_startswith_dash=True,
        words_can_endswith_dash=True,
        words_can_contain_dash=True,
   ):
       """Text files spellchecker function.

       Parameters
       ----------

       filenames : list
         List of path globs to check.

       languages : list
         Languages to use excluding words from being considered mispelling
         errors.

       personal_dicts : list, optional
         Personal dictionaries used to exclude certain words from being
         considered mispelling errors.

       negotiate_languages : bool, optional
         If ``True``, you can pass territory codes as dictionary names, for
         example ``"es"`` instead of ``"es_ES"``.

       encoding : str, optional
         Input encoding. If not defined, it will be autodetected by hunspell.

       include_filename : bool, optional
         Include the filename in which has been found a mispelling error.

       include_line_number : bool, optional
         Include the line number in which has been found a mispelling error.

       include_word : bool, optional
         Include the mispelled word in each mispelling error message.

       include_word_line_index : bool, optional
         Include the index of the caracter in which the mispelled word starts
         in their line (starting at index 0).

       include_line : bool, optional
         Include the entire line where each mispelled word resides.

       include_text : bool, optional
         Include the full text in where the mispelled word resides.

       include_error_number : bool, optional
         Include the number of the error in yielded data. This could be useful
         to avoid the need of define a counter.

       include_near_misses : bool, optional
         Include a list with the near misses for the mispelled word.

       digits_are_words : bool, optional
         If ``False``, values with all characters as digits will not be
         considered words, so they will not be checked for mispelling errors.

       words_can_contain_digits : bool, optional
         If ``False``, values with at least one digit character will not be
         considered words, so they will not be checked for mispelling errors.

       words_can_startswith_dash : bool, optional
         If ``False``, values starting with the ``-`` character will not be
         considered words, so they will not be checked for mispelling errors.

       words_can_endswith_dash : bool, optional
         If ``False``, values ending with the ``-`` character will not be
         considered words, so they will not be checked for mispelling errors.

       words_can_contain_dash : bool, optional
         If ``False``, values containing the ``-`` character will not be
         considered words, so they will not be checked for mispelling errors.
       """
        assert_is_valid_dictionary_language_or_filename(
            languages,
            negotiate_languages=negotiate_languages,
        )

        filename_contents = {}
        for glob_files in files:
             for filename in glob.glob(glob_files):
                 filename_contents[filename] = txt_file_to_content(
                     filename,
                     encoding=encoding,
                 )

        yield from HunspellChecker(
            filename_contents,
            languages,
            personal_dicts=personal_dicts,
            looks_like_a_word=looks_like_a_word_creator(
               digits_are_words=digits_are_words,
               words_can_contain_digits=words_can_contain_digits,
               words_can_startswith_dash=words_can_startswith_dash,
               words_can_endswith_dash=words_can_endswith_dash,
               words_can_contain_dash=words_can_contain_dash,
            ),
            encoding=encoding,
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

.. rubric:: Input

.. code-block::

   hello hola

.. code-block:: python

   for word_error in txt_spell(["foo.txt"], "es_ES"):
       print(word_error)

.. rubric:: Output

.. code-block:: python

   {'filename': 'foo.txt', 'line_number': 1, 'word': 'hello', 'word_line_index': 0}

.. seealso::

   :ref:`hunspellcheck-public-api`
