# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""The environment variables of the project."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Final

import platformdirs
from beartype.typing import Optional, Union
from returns.maybe import Maybe

from python_whiteprint.cli.exceptions import (
    BOOLEAN_STRING,
    NotAValidBooleanError,
)
from python_whiteprint.cli.types import DefaultVenvBackend, LogLevel


__all__: Final = ["DEFAULTS", "str2bool"]


@dataclass(frozen=True)  # pragma: no branch
class _DefaultsLog:
    """Holds the project log default values."""

    level: LogLevel
    file: Optional[Path]


@dataclass(frozen=True)  # pragma: no branch
class _DefaultsCopier:
    """Holds the Copier default values."""

    repository: str
    vcs_ref: Optional[str]
    user_defaults: Optional[Path]
    data: Path


@dataclass(frozen=True)  # pragma: no branch
class _DefaultsPostProcessing:
    """Holds the post processing default values."""

    default_venv_backend: DefaultVenvBackend
    skip_tests: bool
    python: Optional[str]
    github_token: Optional[str]
    https_origin: bool


@dataclass(frozen=True)  # pragma: no branch
class _Defaults:
    """Holds the project default values."""

    log: _DefaultsLog
    copier: _DefaultsCopier
    post_processing: _DefaultsPostProcessing


def str2bool(value: Union[str, bool]) -> bool:
    """Convert a string to a boolean.

    Recognizes "yes", "true", "y", "t", "1" as True, and "no", "false", "n",
    "f", "0" as False.

    Args:
        value: the string to convert.

    Raises:
        NotAValidBooleanError: the value is not one of "yes", "true", "y",
            "t", "1", "no", "false", "n", "f" pr "0".

    Returns:
        the boolean represented by value.
    """
    if isinstance(value, bool):
        return value

    standardized_value = value.lower()
    if standardized_value in BOOLEAN_STRING.true:
        return True

    if standardized_value in BOOLEAN_STRING.false:
        return False

    raise NotAValidBooleanError(value)


DEFAULTS: Final = _Defaults(
    log=_DefaultsLog(
        level=LogLevel(os.environ.get("WHITEPRINT_LOG_LEVEL", "ERROR")),
        file=(
            Maybe.from_optional(os.environ.get("WHITEPRINT_LOG_FILE"))
            .map(Path)
            .value_or(None)
        ),
    ),
    copier=_DefaultsCopier(
        repository=os.environ.get(
            "WHITEPRINT_REPOSITORY",
            "gh:RomainBrault/python-whiteprint.git",
        ),
        vcs_ref=os.environ.get("WHITEPRINT_VCS_REF"),
        user_defaults=(
            Maybe.from_optional(os.environ.get("WHITEPRINT_USER_DEFAULTS"))
            .map(Path)
            .value_or(None)
        ),
        data=Path(
            os.environ.get(
                "WHITEPRINT_DATA",
                (
                    Path(platformdirs.user_config_dir("whiteprint"))
                    / "config.yml"
                ),
            )
        ),
    ),
    post_processing=_DefaultsPostProcessing(
        default_venv_backend=DefaultVenvBackend(
            os.environ.get("WHITEPRINT_DEFAULT_VENV_BACKEND", "VIRTUALENV")
        ),
        skip_tests=str2bool(os.environ.get("WHITEPRINT_SKIP_TESTS", False)),
        python=os.environ.get("WHITEPRINT_PYTHON"),
        github_token=os.environ.get("WHITEPRINT_GITHUB_TOKEN"),
        https_origin=str2bool(
            os.environ.get("WHITEPRINT_HTTPS_ORIGIN", False)
        ),
    ),
)
"""The default values of the project based on environments variables."""
