{% include "jinja_template/license_header.py.j2" %}
"""Types for the CLI."""

import enum
from typing import Final


__all__: Final = ["LogLevel"]


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

    def __str__(self) -> str:
        """Force good enum format when printing help.

        See Also:
            https://github.com/tiangolo/typer/issues/290
        """
        return self.value
