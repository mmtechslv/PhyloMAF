# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath("../"))


# -- Project information -----------------------------------------------------

project = "PhyloMAF"
copyright = "2021, Farid Musa"
author = "Farid Musa"

# The full version, including alpha/beta/rc tags
release = "1.0"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
    "sphinx.ext.autosectionlabel",
    #'sphinx_automodapi.automodapi',
    #'sphinx_automodapi.smart_resolver',
    "autoapi.extension",
    "sphinx.ext.coverage",
    #'sphinx.ext.autodoc.typehints',
    #'sphinx_autodoc_typehints',
    "sphinx-prompt",
    "sphinx_copybutton",
    "sphinx_last_updated_by_git",
    'sphinx_git',
    'hoverxref.extension',
    'sphinxcontrib.bibtex',
    "sphinx_rtd_theme",
]

# Napoleon Configs
napoleon_google_docstring = True
napoleon_use_param = True
napoleon_use_ivar = True

# InterSphinx Configs
intersphinx_mapping = {
    "biom": ("https://biom-format.org/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "python": ("https://docs.python.org/3/", None),
}

# Autosummary Configs
autosummary_generate = True

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

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = "PhyloMAF - Phylogenetic Microbiome Analysis Framework"
# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = "PhyloMAF documentation"
# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = "favicon.ico"
# If false, no module index is generated.
html_use_modindex = True
# Output file base name for HTML help builder.
htmlhelp_basename = "PhyloMAF-doc"
# The name of an image file (relative to this directory) to place at the top of
# the title page.
latex_logo = "phylomaf_logo.png"
# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True
# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False
# This config enables processing of __init__ docstrings
autoclass_content = "both"
# Group members
autodoc_member_order = "groupwise"
# Autodoc options
autoapi_options = [
    "inherited-member",
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
]
autoapi_dirs = ["../pmaf"]
autoapi_ignore = ["*_externals*", "*tests*"]
autoapi_python_class_content = "both"
autoapi_member_order = "groupwise"
autodoc_typehints = "description"
autoapi_add_toctree_entry = False # Add TOC manually
autoapi_keep_files = True # Keep the source files after build.

# Automodapi Configs
numpydoc_show_class_members = False
automodsumm_inherited_members = True

# Configurations for sphinx-hoverxref
hoverxref_role_types = {
    "hoverxref": "modal",
    "ref": "modal",  # for hoverxref_auto_ref config
    "confval": "tooltip",  # for custom object
    "mod": "tooltip",  # for Python Sphinx Domain
    "class": "tooltip",  # for Python Sphinx Domain
}

# Bibtex Configuration
bibtex_bibfiles = ['refs.bib']

#Autosectionlabel configs
autosectionlabel_maxdepth = 1
autosectionlabel_prefix_document = True
