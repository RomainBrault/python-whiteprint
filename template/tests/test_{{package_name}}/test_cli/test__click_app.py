{% include "jinja_template/license_header.py.j2" %}
"""Test the Click app."""

import importlib

from beartype import beartype


@beartype
def test_import_click_app() -> None:
    """Test that we can import a click app."""
    assert importlib.import_module(
        "{{package_name}}.cli._click_app"
    ).click_app, "Click app not found."
