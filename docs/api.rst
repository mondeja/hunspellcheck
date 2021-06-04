.. _hunspellcheck-public-api:

**********
Public API
**********

CLI utilities
~~~~~~~~~~~~~

.. autofunction:: hunspellcheck.hunspellchecker_argument_parser

Spellchecker interface
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: hunspellcheck.HunspellChecker
   :members:

.. autofunction:: hunspellcheck.render_hunspell_word_error
.. autofunction:: hunspellcheck.word.looks_like_a_word_creator

Hunspell utilities
~~~~~~~~~~~~~~~~~~

.. autofunction:: hunspellcheck.get_hunspell_version
.. autofunction:: hunspellcheck.is_valid_dictionary_language
.. autofunction:: hunspellcheck.is_valid_dictionary_language_or_filename
.. autofunction:: hunspellcheck.assert_is_valid_dictionary_language_or_filename
.. autofunction:: hunspellcheck.gen_available_dictionaries
.. autofunction:: hunspellcheck.gen_available_dictionaries_with_langcodes
.. autofunction:: hunspellcheck.list_available_dictionaries
.. autofunction:: hunspellcheck.print_available_dictionaries
