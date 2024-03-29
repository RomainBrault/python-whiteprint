{% include "jinja_template/license_header.py.j2" %}
"""Sphinx configuration."""

# pylint: disable=invalid-name,redefined-builtin


project = "{{project_name}}"
author = "{{author}}"
copyright = "2018-{% now 'utc', '%Y' %}, {{author}}"
myst_heading_anchors = 3
extensions = [
    "autoapi.extension",
    "myst_parser",
    "sphinx_click",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
]
autoapi_type = "python"
autoapi_dirs = ["../src"]
autodoc_typehints = "description"
html_theme = "furo"
html_favicon = "images/favicon.png"
html_logo = "images/logo.png"
html_extra_path = ["images/"]
intersphinx_mapping = {
    "nox": ("https://nox.thea.codes/en/stable", None),
    "pip": ("https://pip.pypa.io/en/stable", None),
    "mypy": ("https://mypy.readthedocs.io/en/stable/", None),
}
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "substitution",
]
