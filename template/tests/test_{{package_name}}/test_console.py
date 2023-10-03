{% include "jinja_template/license_header.py.j2" %}
"""Test the console module."""

from rich import console as rich_console

from {{package_name}} import console as {{package_name}}_console


def test_default_console() -> None:
    """Check that the console is a rich console instance."""
    assert isinstance({{package_name}}_console.DEFAULT, rich_console.Console)
