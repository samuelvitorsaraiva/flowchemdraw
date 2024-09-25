# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# -- Path setup --------------------------------------------------------------

# sphinx-apidoc -o code_structure ../src

import datetime
import os
import sys

sys.path.insert(0, os.path.abspath("../src"))
print(sys.path)


CONF_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
ROOT_DIR = os.path.abspath(os.path.join(CONF_DIR, os.pardir))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


project = "flowchemdraw"
YEAR = datetime.date.today().strftime("%Y")
author = "Flowchem Lab - MPIKG/MPI"
copyright = f"{YEAR}, {author}"
release = ''

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx_design",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinxcontrib.openapi",
    "sphinxcontrib.httpdomain",
]

source_suffix = [".rst", ".md"]
autodoc_member_order = "bysource"

#autodoc_mock_imports = [os.path.abspath("../flowchem")]

# Add any paths that contain templates here, relative to this directory.
#templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

myst_enable_extensions = [
    # "amsmath",
    "colon_fence",
    "deflist",
    # "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


# -- Options for HTML output -------------------------------------------------
# html_logo = "http://placekitten.com/200/90"
#html_theme = "furo"
#html_theme_options = {
#    "light_css_variables": {
#        "primary-color": "#005555",
#    },
#    "dark_css_variables": {
#        "primary-color": "#e5c07b",
#    },
#}
#html_show_copyright = False
#html_show_sphinx = False

#html_static_path = ["_static"]
#html_css_files = [
#    "flowchem.css",
#]