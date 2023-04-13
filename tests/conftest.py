# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Shared test configuration file."""

import pathlib

import pygit2
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


@pytest.fixture()
@beartype
def whiteprint_repository(tmp_path: pathlib.Path) -> pathlib.Path:
    """Clone python_whiteprint local repository into a temporary directory.

    Args:
        tmp_path: a temporary directory in which the repository is cloned.

    Returns:
        A path to the cloned repository.
    """
    destination = (tmp_path / "whiteprint").resolve()
    pygit2.clone_repository(".", str(destination))
    return destination
