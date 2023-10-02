# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""A click command-line interface.

A click app is exposed for auto-documentation purpose with sphinx-click. It
must be defined after the CLI is fully constructed.
"""

from typing import Final

from typer import main

from python_whiteprint.cli.entrypoint import __app__


__all__: Final = ["__click_app__"]
"""Public module attributes."""


__click_app__: Final = main.get_command(__app__)
"""A Click app obtained from the Typer app.

See Also:
    https://typer.tiangolo.com/tutorial/using-click/

Example:
    >>> from python_whiteprint.cli._click_app import __click_app__
    >>>
    >>> assert __click_app__.name
    "whiteprint"
"""
