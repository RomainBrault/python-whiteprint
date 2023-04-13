# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Logging configuration for the CLI."""

import importlib

from beartype import beartype

from python_whiteprint.cli.type import LogLevel


@beartype
def configure_logging(level: LogLevel) -> None:
    """Configure Rich logging handler.

    Args:
        level: The logging verbosity level.

    Example:
        >>> from python_whiteprint.cli.type import LogLevel
        >>>
        >>> configure_logging(LogLevel.INFO)
        None

    See Also:
        https://rich.readthedocs.io/en/stable/logging.html
    """
    logging = importlib.import_module("logging")
    logging.basicConfig(
        level=level.value.upper(),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            importlib.import_module("rich.logging").RichHandler(
                rich_tracebacks=True,
                tracebacks_suppress=[
                    importlib.import_module("beartype"),
                    importlib.import_module("click"),
                    importlib.import_module("typer"),
                ],
            ),
        ],
    )
    logging.captureWarnings(True)
