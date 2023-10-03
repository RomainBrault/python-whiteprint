{% include "jinja_template/license_header.py.j2" %}
"""Manage a global rich console."""

from typing import Final

from rich import console


__all__: Final = ["DEFAULT"]
"""Public module attributes."""


DEFAULT: Final = console.Console()
"""A high level console interface instance.

See Also:
    https://rich.readthedocs.io/en/stable/reference/console.html
"""
