{% include "jinja_template/license_header.py.j2" %}
"""Logging configuration for the CLI."""

import importlib
from pathlib import Path
from typing import Final

from beartype.typing import Optional
from returns.maybe import Maybe

from {{package_name}} import console
from {{package_name}}.cli.types import LogLevel
from {{package_name}}.loc import _


__all__: Final = ["configure_logging"]


def configure_logging(
    level: LogLevel,
    *,
    filename: Optional[Path] = None,
    log_format: str = _(
        "[{process}:{thread}] [{pathname}:{funcName}:{lineno}]\n{message}"
    ),
    date_format: str = _("[%Y-%m-%dT%H:%M:%S]"),
) -> None:
    """Configure Rich logging handler.

    Args:
        level: The logging verbosity level.
        filename: An optional filename in which to log. If None, log on the
            standard output.
        fmt: The log format.
        date_format: The log date format.

    Example:
        >>> from {{package_name}}.cli.types import LogLevel
        >>>
        >>> configure_logging(LogLevel.INFO)
        None

    See Also:
        https://rich.readthedocs.io/en/stable/logging.html
    """
    logging = importlib.import_module("logging")
    logging.basicConfig(
        **(
            Maybe.from_optional(filename)
            .map(
                lambda filename: {
                    "filename": str(filename.resolve()),
                    "format": "{asctime} " + log_format,
                }
            )
            .or_else_call(
                lambda: {
                    "handlers": [
                        importlib.import_module("rich.logging").RichHandler(
                            console=console.DEFAULT,
                            rich_tracebacks=True,
                            tracebacks_suppress=[
                                importlib.import_module("click"),
                                importlib.import_module("typer"),
                            ],
                        ),
                    ],
                    "format": log_format,
                }
            )
        ),
        level=level.value.upper(),
        datefmt=date_format,
        style="{",
    )
    logging.captureWarnings(True)
