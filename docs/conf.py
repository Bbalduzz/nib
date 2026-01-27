# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# -- Path setup --------------------------------------------------------------

# Add the Python source directory to the path so autodoc can find the modules
sys.path.insert(0, os.path.abspath("../python"))

# -- Project information -----------------------------------------------------

project = "Nib"
copyright = "2026, Nib Contributors"
author = "Nib Contributors"
release = "0.1.0"
version = "0.1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    "sphinx_autodoc_typehints",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The master toctree document
master_doc = "index"

# -- Options for autodoc -----------------------------------------------------

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
    "show-inheritance": True,
}

# Include both class and __init__ docstrings
autoclass_content = "both"

# Generate autosummary stubs
autosummary_generate = True

# -- Options for Napoleon (Google-style docstrings) --------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None
napoleon_attr_annotations = True

# -- Options for sphinx-autodoc-typehints ------------------------------------

typehints_fully_qualified = False
always_document_param_types = True
typehints_document_rtype = True

# -- Options for intersphinx -------------------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# -- Options for HTML output -------------------------------------------------

html_theme = "revitron_sphinx_theme"

html_theme_options = {
    "color_scheme": "",
    "canonical_url": "",
    "style_external_links": True,
    "collapse_navigation": False,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
    "github_url": "",
    "logo_mobile": "",
}

html_static_path = ["_static"]
html_css_files = []

# -- Options for viewcode extension ------------------------------------------

viewcode_follow_imported_members = True

# -- Custom setup ------------------------------------------------------------


def setup(app):
    """Custom Sphinx setup."""
    pass
