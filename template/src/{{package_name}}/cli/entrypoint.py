{% include "jinja_template/license_header.py.j2" %}
"""Command Line Interface."""

import importlib
from pathlib import Path
from typing import Final

from beartype.typing import Optional
from typer import main, params
from typing_extensions import Annotated

from {{package_name}}.cli._callback import cb_version
from {{package_name}}.cli.environment import DEFAULTS
from {{package_name}}.cli.types import LogLevel
from {{package_name}}.loc import _


__all__: Final = ["__app__", "__app_name__", "callback"]
"""Public module attributes."""


__app_name__: Final = "{{project_slug}}"
"""The name of the application."""

__app__ = main.Typer(
    name=__app_name__,
    add_completion=False,
)
"""The command-line interface."""


@__app__.command(
    name="main",
    help=_("Print 'Hello, World!' to the standard output."),
)
def callback(
    *,
    log_level: Annotated[
        LogLevel,
        params.Option(
            "-l",
            "--log-level",
            case_sensitive=False,
            help=_("Logging verbosity."),
            envvar="{{package_name.upper()}}_LOG_LEVEL",
        ),
    ] = DEFAULTS.log_level,
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
            envvar="{{package_name.upper()}}_LOG_FILE",
        ),
    ] = DEFAULTS.log_file,
    _version: Annotated[
        bool,
        params.Option(
            "-v",
            "--version",
            callback=cb_version,
            is_eager=True,
            help=_(
                "Print the version number of the application to the standard"
                " output and exit."
            ),
        ),
    ] = False,
) -> None:
    """Print 'Hello, World!' to the standard output.

    Args:
        log_level: The logging verbosity level.
        _version: A callback printing the CLI's version number.
    """
    # We perform a lazy import of the hello_world module to improve the CLI's
    # responsiveness.
    importlib.import_module(
        "{{package_name}}.cli._logging",
        __package__,
    ).configure_logging(level=log_level, filename=log_file)
    importlib.import_module(
        "{{package_name}}.hello_world",
        __package__,
    ).hello_world()
