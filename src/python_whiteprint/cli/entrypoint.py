# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Command Line Interface app entrypoint."""

import importlib
from pathlib import Path
from typing import Final

from beartype.typing import Optional
from typer import main, params
from typing_extensions import Annotated

from python_whiteprint.cli import _callback, init
from python_whiteprint.cli.environment import DEFAULTS
from python_whiteprint.cli.types import LogLevel
from python_whiteprint.loc import _


__all__: Final = ["__app__", "__app_name__", "callback"]
"""Public module attributes."""


__app_name__: Final = "whiteprint"
"""The name of the application."""


__app__ = main.Typer(
    name=__app_name__,
    add_completion=True,
    no_args_is_help=True,
    epilog=_("Each sub-command has its own --help."),
    help=_(
        "Thank you for using {}, a tool to generate minimal Python projects."
    ).format(__app_name__),
)
"""The Typer app.

See Also:
    https://typer.tiangolo.com/tutorial/package/

Example:
    >>> from python_whiteprint.cli.entrypoint import __app__
    >>>
    >>> assert __app__.info.name == "whiteprint"
"""


@__app__.callback()
def callback(
    *,
    log_level: Annotated[
        LogLevel,
        params.Option(
            "-l",
            "--log-level",
            case_sensitive=False,
            help=_("Logging verbosity."),
            envvar="WHITEPRINT_LOG_LEVEL",
        ),
    ] = DEFAULTS.log.level,
    log_file: Annotated[
        Optional[Path],
        params.Option(
            "--log-file",
            exists=False,
            file_okay=True,
            dir_okay=False,
            writable=True,
            readable=False,
            resolve_path=True,
            help=_(
                "A file in which to write the log. If None, logs are"
                " written on the standard output."
            ),
            envvar="WHITEPRINT_LOG_FILE",
        ),
    ] = DEFAULTS.log.file,
    _version: Annotated[
        bool,
        params.Option(
            "-v",
            "--version",
            callback=_callback.cb_version,
            is_eager=True,
            help=_(
                "Print the version number of the application to the standard"
                " output and exit."
            ),
        ),
    ] = False,
) -> None:
    """CLI callback.

    Args:
        log_level: The logging verbosity level.
        log_file: A file in which to write the log. If None, logs are written
            on the standard output.
        _version: A callback printing the CLI's version number.

    See Also:
        https://typer.tiangolo.com/tutorial/commands/callback/
    """
    importlib.import_module(
        "python_whiteprint.cli._logging",
        __package__,
    ).configure_logging(level=log_level, filename=log_file)


__app__.command(
    epilog=_(
        "This command mostly forwards copier's CLI. For more details see"
        " https://copier.readthedocs.io/en/stable/reference/cli/#copier.cli.CopierApp."
    ),
    help=_("Initalize a new Python project."),
)(init.init)
