# SPDX-FileCopyrightText: 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Shared test configuration file."""
import pytest
from beartype import beartype
from typer import testing


@beartype
@pytest.fixture(scope="class")
def cli_runner() -> testing.CliRunner:
    """CLI Runner Fixture.

    Returns:
        A CliRunner instance.
    """
    return testing.CliRunner()
