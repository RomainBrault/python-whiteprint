{% include "jinja_template/license_header.py.j2" %}
"""A click command-line interface.

A click app is exposed for auto-documentation purpose with sphinx-click. It
must be defined after the CLI is fully constructed.
"""

from typing import Final

from typer import main

from {{package_name}}.cli.entrypoint import __app__


__all__: Final = ["__click_app__"]
"""Public module attributes."""


__click_app__: Final = main.get_command(__app__)
"""A Click app obtained from the Typer app.

See Also:
    https://typer.tiangolo.com/tutorial/using-click/

Example:
    >>> from {{package_name}}.cli._click_app import __click_app__
    >>>
    >>> __click_app__.name
    "{{project_slug}}"
"""
