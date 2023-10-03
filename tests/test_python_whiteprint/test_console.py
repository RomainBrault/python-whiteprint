# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Test the console module."""

from rich import console as rich_console

from python_whiteprint import console as python_whiteprint_console


def test_default_console() -> None:
    """Check that the console is a rich console instance."""
    assert isinstance(python_whiteprint_console.DEFAULT, rich_console.Console)
