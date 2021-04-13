"""Configuration file for the Sphinx documentation builder for mdpo."""

import datetime
import os
import sys


# -- Path setup --------------------------------------------------------------

sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------
project = "hunspellcheck"
author = "Álvaro Mondéjar Rubio"
copyright = f"2020, {author}"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx_github_changelog",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_css_files = [
    os.path.join("css", "override-styles.css"),
]

# -- Options for `sphinx.ext.intersphinx` ------------------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_preprocess_types = True


# -- Options for `sphinx.ext.intersphinx` ------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "jinja2": ("https://jinja2docs.readthedocs.io/en/stable", None),
    "babel": ("http://babel.pocoo.org/en/latest", None),
    "hunspellcheck": ("http://hunspellcheck.readthedocs.io/en/latest", None),
}
