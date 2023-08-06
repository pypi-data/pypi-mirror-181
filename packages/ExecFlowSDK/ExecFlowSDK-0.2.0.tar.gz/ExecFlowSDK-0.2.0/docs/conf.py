# pylint: disable=missing-docstring,similarities,fixme,invalid-name,redefined-builtin
import os

import execflow

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "ExecFlow SDK"
copyright = "© SINTEF 2022"
author = "SINTEF"
version = ".".join(execflow.__version__.split(".")[:2])  # Short X.Y version
release = execflow.__version__
# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# General configuration
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**.ipynb_checkpoints",
    "attic/**/*",
    "_templates",
]

extensions = [
    "myst_nb",  # markdown source support & support for Jupyter notebooks
    "autoapi.extension",
    "sphinx.ext.graphviz",
    "sphinx.ext.intersphinx",  # Connect to external Sphinx documentation
    "sphinx.ext.napoleon",  # API ref Google and NumPy style
    "sphinx.ext.viewcode",
    "sphinxcontrib.plantuml",
    "sphinx_copybutton",  # Copy button for codeblocks
    "sphinx_design",
]

root_doc = "index"

suppress_warnings = ["myst.mathjax"]

# Extension configuration
autoapi_dirs = ["../execflow"]
autoapi_type = "python"
autoapi_file_patterns = ["*.py", "*.pyi"]
autoapi_template_dir = "_templates/autoapi"
autoapi_add_toctree_entry = True  # Toggle the most top-level index file
autoapi_options = [
    "members",
    "undoc-members",
    "private-members",
    "show-inheritance",
    "show-module-summary",
    "special-members",
    "imported-members",
    "show-inheritance-diagram",
    # "inherited-members",
]
autoapi_keep_files = False  # Should be False in production

autodoc_typehints = "description"
autodoc_typehints_format = "short"
autodoc_inherit_docstrings = True

# HTML output
html_theme = "sphinx_book_theme"
html_logo = "_static/logo.jpeg"
html_favicon = "_static/favicon.ico"
html_theme_options = {
    "path_to_docs": "docs",
    "repository_url": "https://github.com/H2020-OpenModel/WP3-WrapperSDK",
    "repository_branch": "master",
    "use_issues_button": True,
    "use_fullscreen_button": True,
    "use_repository_button": True,
    "logo_only": True,
    "show_navbar_depth": 1,
    # "announcement": "This is an announcement!",
}
html_static_path = ["_static"]
# html_css_files = ["custom.css"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "aiida": ("https://aiida.readthedocs.io/projects/aiida-core/en/latest", None),
    "oteapi": ("https://emmc-asbl.github.io/oteapi-core/latest/", None),
}

myst_heading_anchors = 5
myst_enable_extensions = ["colon_fence"]

napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_preprocess_types = True
napoleon_attr_annotations = True

nb_execution_allow_errors = False
nb_execution_mode = "cache"
if os.getenv("CI"):
    nb_kernel_rgx_aliases = {".*": "python"}

plantuml = "java -jar lib/plantuml.jar"
plantuml_output_format = "svg_img"
