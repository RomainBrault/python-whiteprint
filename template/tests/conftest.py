{% include "jinja_template/license_header.py.j2" %}
"""Shared test configuration file."""

import pytest
from beartype import beartype
from typer import testing


@pytest.fixture(scope="class")
@beartype
def cli_runner() -> testing.CliRunner:
    """CLI Runner Fixture.

    Returns:
        A CliRunner instance.
    """
    return testing.CliRunner()
