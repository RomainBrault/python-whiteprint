# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Manage a global rich console."""

from rich import console


DEFAULT = console.Console()
"""A high level console interface instance.

See Also:
    https://rich.readthedocs.io/en/stable/reference/console.html
"""
