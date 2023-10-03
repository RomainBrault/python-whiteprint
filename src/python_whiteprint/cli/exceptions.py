# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Command-Line Interface user defined exceptions."""

from dataclasses import dataclass
from pathlib import Path
from typing import Final

from beartype.typing import Set
from click.exceptions import UsageError


__all__: Final = [
    "NotAValidBooleanError",
    "UnsupportedTypeInMappingError",
    "NotAValidYAMLError",
]


@dataclass(frozen=True)  # pragma: no branch
class BooleanSring:
    """Holds the sets of strings reprensenting a boolean."""

    true: Set[str]
    false: Set[str]


BOOLEAN_STRING: Final = BooleanSring(
    true={"1", "yes", "y", "true", "t"},
    false={"0", "no", "n", "false", "f"},
)
"""Strings representings a boolean."""


class NotAValidBooleanError(UsageError):
    """A string does not represent a valid boolean."""

    def __init__(self, value: str) -> None:
        """Initialize the exception."""
        super().__init__(
            f"{value} is not a valid boolean.  It should be one of"
            f" {BOOLEAN_STRING.true} to represent a true value or one of"
            f" {BOOLEAN_STRING.false} to represent a false value."
        )


class UnsupportedTypeInMappingError(UsageError):
    """The given type is not supported."""

    def __init__(self) -> None:
        """Initialize the exception."""
        super().__init__("The mapping contains unsupported type.")


class NotAValidYAMLError(UsageError):
    """The YAML file is invalid."""

    def __init__(self, path: Path, error: str) -> None:
        """Initialize the exception.

        Args:
            path: path to the invalid YAML file.
            error: the parser error message.
        """
        super().__init__(f"{path} is not a valid YAML file, {error}.")
