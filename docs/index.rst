#############################
hunspellcheck's documentation
#############################

This library is a helper for writing spell checkers using hunspell.

If you want to standarize the execution and writing of several spell checkers
for different file types, performing the spell checking against ortographic
dictionaries, this library is for you. It will allow you to reuse some patterns
repeated using hunspell for spell checking.

********
Features
********

* Graceful handling of missing dictionaries.
* Custom dictionaries by filepath.
* Multiple personal dictionaries by filepath.
* Argument parsers building.
* Well tested system calls to `hunspell`.
* Well defined programatic interface for spellcheckers.

.. toctree::
   :maxdepth: 3
   :caption: Manual

   install
   tutorial

.. toctree::
   :maxdepth: 3
   :caption: Reference

   api
