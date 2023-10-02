{% include "jinja_template/license_header.py.j2" %}
"""Shared test configuration file."""

import pytest
from typer import testing


@pytest.fixture(scope="class")
def cli_runner() -> testing.CliRunner:
    """CLI Runner Fixture.

    Returns:
        A CliRunner instance.
    """
    return testing.CliRunner(mix_stderr=False)
