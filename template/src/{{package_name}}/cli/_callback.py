{% include "jinja_template/license_header.py.j2" %}
"""Callbacks for the CLI."""

import importlib

from beartype import beartype


@beartype
def cb_version(*, value: bool) -> None:
    """A typer callback that prints the package's version.

    If value is true, print the version number. Exit the app right after.

    Args:
        value:
            Whether the callback is executed or not.
    """
    if not value:
        return

    importlib.import_module(
        "{{package_name}}.console",
        __package__,
    ).DEFAULT.print(
        importlib.import_module(
            "{{package_name}}.version",
            __package__,
        ).__version__
    )

    raise importlib.import_module("click.exceptions").Exit
