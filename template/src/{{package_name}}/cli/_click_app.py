{% include "jinja_template/license_header.py.j2" %}
"""A click command-line interface.

A click app is exposed for auto-documentation purpose with sphinx-click. It
must be defined after the CLI is fully constructed.
"""

from typer import main

from {{package_name}}.cli.entrypoint import app


click_app = main.get_command(app)
"""A Click app obtained from the Typer app.

See Also:
    https://typer.tiangolo.com/tutorial/using-click/

Example:
    >>> from python_whiteprint.cli._click_app import click_app
    >>>
    >>> click_app.name
    "whiteprint"
"""
