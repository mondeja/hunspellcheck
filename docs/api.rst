**********
Public API
**********

.. rubric:: CLI utilities

.. autofunction:: hunspellcheck.extend_argument_parser

.. rubric:: Spellchecker interface

.. autoclass:: hunspellcheck.HunspellChecker
   :members:

.. autofunction:: hunspellcheck.render_hunspell_word_error
.. autofunction:: hunspellcheck.looks_like_a_word

.. rubric:: Hunspell utilities

.. autofunction:: hunspellcheck.get_hunspell_version
.. autofunction:: hunspellcheck.is_valid_dictionary_language
.. autofunction:: hunspellcheck.is_valid_dictionary_language_or_filename
.. autofunction:: hunspellcheck.assert_is_valid_dictionary_language_or_filename
.. autofunction:: hunspellcheck.gen_available_dictionaries
.. autofunction:: hunspellcheck.gen_available_dictionaries_with_langcodes
.. autofunction:: hunspellcheck.list_available_dictionaries
.. autofunction:: hunspellcheck.print_available_dictionaries
