{% include "jinja_template/license_header.py.j2" %}
"""Types for the CLI."""

import enum


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
