{% include "jinja_template/license_header.py.j2" %}
"""Manage a global rich console."""

from rich import console


DEFAULT = console.Console()
"""A high level console interface instance.

See Also:
    https://rich.readthedocs.io/en/stable/reference/console.html
"""
