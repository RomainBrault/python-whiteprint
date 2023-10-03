# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Command-Line Interface user defined types."""

import enum
from typing import Final

from beartype.typing import Dict, Union


__all__: Final = ["LogLevel", "DefaultVenvBackend"]


Yaml = Dict[str, Union[str, int]]


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


class DefaultVenvBackend(str, enum.Enum):
    """Nox's default virtual environments backend."""

    NONE = "NONE"
    VIRTUALENV = "VIRTUALENV"
    CONDA = "CONDA"
    MAMBA = "MAMBA"
    VENV = "VENV"
