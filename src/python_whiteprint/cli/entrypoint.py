# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Command Line Interface app entrypoint."""

import importlib
from os import environ

from beartype import beartype
from typer import main, params

from python_whiteprint.cli import _callback, init
from python_whiteprint.cli.type import LogLevel
from python_whiteprint.loc import _


app = main.Typer(
    name="whiteprint",
    add_completion=True,
    no_args_is_help=True,
    epilog=_("Any command has its own --help."),
    help=_("Thank you for using Whiteprint!"),
)
"""The Typer app.

See Also:
    https://typer.tiangolo.com/tutorial/package/

Example:
    >>> from python_whiteprint.cli.entrypoint import app
    >>>
    >>> assert app.info.name == "whiteprint"
"""


_option_version = params.Option(
    False,
    "--version",
    callback=_callback.cb_version,
    is_eager=True,
    help=_(
        "Print the version number of the application to the standard output "
        "and exit."
    ),
)
"""see `python_whiteprint.cli.entrypoint.callback` option `version`."""
_option_log_level = params.Option(
    environ.get("WHITEPRINT_LOG_LEVEL", "ERROR"),
    "--log-level",
    case_sensitive=False,
    help=_("Logging verbosity."),
    envvar="WHITEPRINT_LOG_LEVEL",
)
"""see `python_whiteprint.cli.entrypoint.callback` option `log_level`."""


@beartype
@app.callback()
def callback(
    *,
    log_level: LogLevel = _option_log_level,
    _version: bool = _option_version,
) -> None:
    """CLI callback.

    Args:
        log_level: The logging verbosity level.
        _version: A callback printing the CLI's version number.

    See Also:
        https://typer.tiangolo.com/tutorial/commands/callback/
    """
    importlib.import_module(
        "python_whiteprint.cli._logging",
        __package__,
    ).configure_logging(level=log_level)


app.command(
    epilog=_(
        "This command mostly forwards copier's CLI. For more details see"
        " https://copier.readthedocs.io/en/stable/reference/cli/#copier.cli.CopierApp."
    ),
    help=_("Initalize a new Python project."),
)(init.init)
