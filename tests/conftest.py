# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Shared test configuration file."""

import pathlib

import pygit2
import pytest
from beartype import beartype
from beartype.typing import List, TypedDict
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


@beartype
class YAMLAutocomplete(TypedDict):
    """YAML autocomletion diretory content."""

    path: pathlib.Path
    yaml_files: List[str]
    non_yaml_files: List[str]


@pytest.fixture()
@beartype
def autocomplete_dir_yaml(tmp_path: pathlib.Path) -> YAMLAutocomplete:
    """Create a bunch of YAML and non-YAML files into a temporary directory.

    Args:
        tmp_path: a temporary directory in which the repository is cloned.

    Returns:
        A path to the directory containing the YAML files
    """
    autocomplete = YAMLAutocomplete(
        path=tmp_path / "autocomplete",
        yaml_files=["test.yaml", "test.yml"],
        non_yaml_files=["test.txt", "yml", "yml.txt"],
    )
    autocomplete["path"].mkdir()

    for file in autocomplete["non_yaml_files"] + autocomplete["yaml_files"]:
        (autocomplete["path"] / file).touch()

    return autocomplete
