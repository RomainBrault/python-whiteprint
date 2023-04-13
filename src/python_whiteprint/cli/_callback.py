# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

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
        "python_whiteprint.console",
        __package__,
    ).DEFAULT.print(
        importlib.import_module(
            "python_whiteprint.version",
            __package__,
        ).__version__
    )

    raise importlib.import_module("click.exceptions").Exit
