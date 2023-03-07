# SPDX-FileCopyrightText: 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Command Line Interface."""
import enum
import importlib

from beartype import beartype
from click import exceptions
from typer import main, params

from python_whiteprint.loc import _


app = main.Typer(add_completion=False)
"""The command-line interface."""


class LogLevel(str, enum.Enum):
    """Logging levels.

    See Also:
        https://docs.python.org/3/library/logging.html#levels
    """

    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"
    NOTSET = "NOTSET"


@beartype
def _cb_version(*, value: bool) -> None:
    """A typer callback that prints the package's version.

    If value is true, print the version number. Exit the app right after.

    Args:
        value:
            Whether the callback is executed or not.
    """
    if value:
        console = importlib.import_module(
            "python_whiteprint.console",
            __package__,
        )
        version = importlib.import_module(
            "python_whiteprint.version",
            __package__,
        )
        console.DEFAULT.print(version.__version__)
        raise exceptions.Exit


@beartype
def _configure_logging(level: LogLevel) -> None:
    """Configure Rich logging handler.

    Args:
        level: The logging verbosity level.

    Example:
        >>> from python_whiteprint.cli import LogLevel
        >>>
        >>> _configure_logging(LogLevel.INFO)
        None

    See Also:
        https://rich.readthedocs.io/en/stable/logging.html
    """
    importlib.import_module("logging").basicConfig(
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


_version_option = params.Option(
    False,
    "--version",
    callback=_cb_version,
    is_eager=True,
    help=_(
        "Print the version number of the application to the standard output "
        "and exit."
    ),
)
"""The typer option serving as default value for the CLI's version flag."""
_default_log_level = params.Option(
    LogLevel.INFO,
    "--log-level",
    case_sensitive=False,
    help=_("Logging verbosity."),
    envvar="WHITEPRINT_LOG_LEVEL",
)
"""The default logging level of the CLI."""


@beartype
@app.command(name="main")
def _main(
    log_level: LogLevel = _default_log_level,
    *,
    _version: bool = _version_option,
) -> None:
    """Print 'Hello, World!' to the standard output."""
    # We perform a lazy import of the hello_world module to improve the CLI's
    # responsiveness.
    _configure_logging(level=log_level)
    hello_world = importlib.import_module(
        "python_whiteprint.hello_world",
        __package__,
    )
    hello_world.hello_world()


_click_app = main.get_command(app)
"""A click command-line interface.

A click app is exposed for auto-documentation purpose with sphinx-click. It
must be defined after the CLI is fully constructed.
"""
