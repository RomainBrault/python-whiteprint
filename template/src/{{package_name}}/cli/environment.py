{% include "jinja_template/license_header.py.j2" %}

"""The environment variables of the project."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from beartype.typing import Optional, Union
from returns.maybe import Maybe

from {{package_name}}.cli.cli_types import LogLevel


__all__: Final = ["DEFAULTS"]


@dataclass(frozen=True)  # pragma: no branch
class _Defaults:
    """Holds the project default values."""

    log_level: LogLevel
    log_file: Optional[Path]


DEFAULTS: Final = _Defaults(
    log_level=LogLevel(os.environ.get("WHITEPRINT_LOG_LEVEL", "ERROR")),
    log_file=(
        Maybe.from_optional(os.environ.get("WHITEPRINT_LOG_FILE"))
        .map(Path)
        .value_or(None)
    ),
)
"""The default values of the project based on environments variables."""
