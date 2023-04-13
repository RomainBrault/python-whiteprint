{% include "jinja_template/license_header.py.j2" %}
"""Command Line Interface."""

import importlib
from os import environ

from beartype import beartype
from typer import main, params

from {{package_name}}.cli._callback import cb_version
from {{package_name}}.cli.type import LogLevel
from {{package_name}}.loc import _


app = main.Typer(add_completion=False)
"""The command-line interface."""


_option_version = params.Option(
    False,
    "--version",
    callback=cb_version,
    is_eager=True,
    help=_(
        "Print the version number of the application to the standard output "
        "and exit."
    ),
)
"""see `{{package_name}}.cli.entrypoint` option `log_level`."""
_option_log_level = params.Option(
    environ.get("WHITEPRINT_LOG_LEVEL", "INFO"),
    "--log-level",
    case_sensitive=False,
    help=_("Logging verbosity."),
    envvar="WHITEPRINT_LOG_LEVEL",
)
"""see `{{package_name}}.cli.entrypoint` option `log_level`."""


@beartype
@app.command(
    name="main",
    help=_("Print 'Hello, World!' to the standard output."),
)
def callback(
    *,
    log_level: LogLevel = _option_log_level,
    _version: bool = _option_version,
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
    ).configure_logging(level=log_level)
    importlib.import_module(
        "{{package_name}}.hello_world",
        __package__,
    ).hello_world()
