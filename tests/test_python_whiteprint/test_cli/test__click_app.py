# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Test the Click app."""

import importlib

from beartype import beartype


@beartype
def test_import_click_app() -> None:
    """Test that we can import a click app."""
    assert importlib.import_module(
        "python_whiteprint.cli._click_app"
    ).click_app, "Click app not found."
