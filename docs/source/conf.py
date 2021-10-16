import sphinx_rtd_theme

# -- Project information -----------------------------------------------------
author = "Jean-Marc Fontaine"
copyright = "2021 Jean-Marc Fontaine"  # noqa: A001
project = "Pantomath"

# -- General configuration ---------------------------------------------------
extensions = [
    "autoapi.extension",
    "sphinx.ext.autodoc",
]

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# -- Options for AutoAPI -------------------------------------------------
autoapi_dirs = ["../../src/pantomath"]
autoapi_member_order = "alphabetical"
autoapi_options = [
    "imported-members",
    "members",
    "show-inheritance",
    "show-module-summary",
    "special-members",
    "undoc-members",
]
autoapi_root = "api"
autoapi_type = "python"
autodoc_typehints = "description"
