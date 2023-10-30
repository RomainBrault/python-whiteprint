# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Test the init command."""

import os
import pathlib
import sys
import uuid
from typing import Final

import pytest
import yaml
from github import Auth
from typer import testing

from python_whiteprint import git
from python_whiteprint.cli import entrypoint, exceptions, init
from tests.conftest import YAMLAutocomplete


TEST_COPIER: Final = "test_copier"


class TestInit:  # pylint: disable=too-few-public-methods
    """Test the init command."""

    @staticmethod
    def test_default(
        *,
        cli_runner: testing.CliRunner,
        whiteprint_repository: pathlib.Path,
        tmp_path: pathlib.Path,
        python_version: str,
    ) -> None:
        """Check whether the CLI can be invoked with the default options."""
        # Note: we must use the --defaults flag to avoid interactive mode.
        with (defaults := tmp_path / "defaults.yml").open(
            "w",
            encoding="utf-8",
        ) as defaults_file:
            yaml.dump(
                {
                    "project_name": "Test Whiteprint",
                    "author": "Pytest Test",
                    "email": "test@pytest.com",
                    "target_python_version": python_version,
                },
                defaults_file,
            )

        (test_copier := tmp_path / TEST_COPIER).mkdir()
        initial_directory = pathlib.Path.cwd().resolve()
        result = cli_runner.invoke(
            entrypoint.__app__,
            [
                "init",
                "-w",
                str(whiteprint_repository.resolve()),
                "-v",
                "HEAD",
                "--no-data",
                "--user-defaults",
                str(defaults),
                "--defaults",
                str(test_copier.resolve()),
                "--python",
                sys.executable,
            ],
        )
        assert (
            result.exit_code == 0
        ), f"The CLI did not exit properly: {result.stderr}."
        assert (
            initial_directory == pathlib.Path.cwd().resolve()
        ), "Initial and final working directory differ"

    @staticmethod
    def test_skip_tests(
        *,
        cli_runner: testing.CliRunner,
        whiteprint_repository: pathlib.Path,
        tmp_path: pathlib.Path,
        python_version: str,
    ) -> None:
        """Check whether the tests can be skipped."""
        # Note: we must use the --defaults flag to avoid interactive mode.
        with (defaults := tmp_path / "defaults.yml").open(
            "w",
            encoding="utf-8",
        ) as defaults_file:
            yaml.dump(
                {
                    "project_name": "Test Whiteprint",
                    "author": "Pytest Test",
                    "email": "test@pytest.com",
                    "target_python_version": python_version,
                },
                defaults_file,
            )

        (test_copier := tmp_path / TEST_COPIER).mkdir()
        initial_directory = pathlib.Path.cwd().resolve()
        result = cli_runner.invoke(
            entrypoint.__app__,
            [
                "init",
                "-w",
                str(whiteprint_repository.resolve()),
                "-v",
                "HEAD",
                "--skip-tests",
                "--no-data",
                "--user-defaults",
                str(defaults),
                "--defaults",
                str(test_copier.resolve()),
                "--python",
                sys.executable,
            ],
        )
        assert (
            result.exit_code == 0
        ), f"The CLI did not exit properly: {result.stderr}."
        assert (
            initial_directory == pathlib.Path.cwd().resolve()
        ), "Initial and final working directory differ"

    @staticmethod
    @pytest.mark.parametrize("spdx_license", ["MIT", "None"])
    def test_licenses(
        *,
        cli_runner: testing.CliRunner,
        whiteprint_repository: pathlib.Path,
        tmp_path: pathlib.Path,
        spdx_license: str,
        python_version: str,
    ) -> None:
        """Check whether the tests can be skipped."""
        # Note: we must use the --defaults flag to avoid interactive mode.
        with (defaults := tmp_path / "defaults.yml").open(
            "w",
            encoding="utf-8",
        ) as defaults_file:
            yaml.dump(
                {
                    "project_name": "Test Whiteprint",
                    "author": "Pytest Test",
                    "email": "test@pytest.com",
                    "spdx_license": spdx_license,
                    "target_python_version": python_version,
                },
                defaults_file,
            )

        (test_copier := tmp_path / TEST_COPIER).mkdir()
        initial_directory = pathlib.Path.cwd().resolve()
        result = cli_runner.invoke(
            entrypoint.__app__,
            [
                "init",
                "-w",
                str(whiteprint_repository.resolve()),
                "-v",
                "HEAD",
                "--skip-tests",
                "--no-data",
                "--user-defaults",
                str(defaults),
                "--defaults",
                str(test_copier.resolve()),
                "--https-origin",
                "--python",
                sys.executable,
            ],
        )
        assert (
            result.exit_code == 0
        ), f"The CLI did not exit properly: {result.stderr}."
        assert (
            initial_directory == pathlib.Path.cwd().resolve()
        ), "Initial and final working directory differ"

    @staticmethod
    def test_github(
        *,
        cli_runner: testing.CliRunner,
        whiteprint_repository: pathlib.Path,
        tmp_path: pathlib.Path,
        python_version: str,
    ) -> None:
        """Check GitHub integration."""
        with (defaults := tmp_path / "defaults.yml").open(
            "w",
            encoding="utf-8",
        ) as defaults_file:
            project_slug = f"test-whiteprint-{uuid.uuid4()}"
            yaml.dump(
                {
                    "project_name": "Test Whiteprint",
                    "project_slug": project_slug,
                    "author": "Pytest Test",
                    "email": "test@pytest.com",
                    "target_python_version": python_version,
                },
                defaults_file,
            )

        (test_copier := tmp_path / TEST_COPIER).mkdir()
        initial_directory = pathlib.Path.cwd().resolve()

        result = cli_runner.invoke(
            entrypoint.__app__,
            [
                "init",
                "-w",
                str(whiteprint_repository.resolve()),
                "-v",
                "HEAD",
                "--no-data",
                "--user-defaults",
                str(defaults),
                "--defaults",
                str(test_copier.resolve()),
                "--python",
                sys.executable,
            ],
            env={
                "WHITEPRINT_GITHUB_TOKEN": os.environ[
                    "WHITEPRINT_TEST_GITHUB_TOKEN"
                ],
            },
        )
        git.delete_github_repository(
            project_slug,
            token=Auth.Token(os.environ["WHITEPRINT_TEST_GITHUB_TOKEN"]),
        )

        assert (
            result.exit_code == 0
        ), f"The CLI did not exit properly: {result.stderr}."
        assert (
            initial_directory == pathlib.Path.cwd().resolve()
        ), "Initial and final working directory differ"


class TestYAML:  # pylint: disable=too-few-public-methods
    """Test the init command."""

    @staticmethod
    def test_read_valid(
        *,
        tmp_path: pathlib.Path,
        python_version: str,
    ) -> None:
        """Check that it is possible to read a valid YAML file."""
        with (defaults := tmp_path / "defaults.yml").open(
            "w",
            encoding="utf-8",
        ) as defaults_file:
            yaml.dump(
                {
                    "project_name": "Test Whiteprint",
                    "author": "Pytest Test",
                    "email": "test@pytest.com",
                    "target_python_version": python_version,
                },
                defaults_file,
            )

        init.read_yaml(defaults)

    @staticmethod
    def test_read_invalid_type(
        *,
        tmp_path: pathlib.Path,
        python_version: str,
    ) -> None:
        """Check that nested dict yaml raises."""
        with (defaults := tmp_path / "defaults.yml").open(
            "w",
            encoding="utf-8",
        ) as defaults_file:
            yaml.dump(
                {
                    "project_name": "Test Whiteprint",
                    "author": "Pytest Test",
                    "email": "test@pytest.com",
                    "invalid": {"invalid": "invalid"},
                    "target_python_version": python_version,
                },
                defaults_file,
            )

        with pytest.raises(exceptions.UnsupportedTypeInMappingError):
            init.read_yaml(defaults)

    @staticmethod
    def test_read_parser_error(
        *,
        tmp_path: pathlib.Path,
    ) -> None:
        """Check that reading an invalid YAML raises the proper exception."""
        (defaults := tmp_path / "defaults.yml").write_text(r"{")

        with pytest.raises(exceptions.NotAValidYAMLError):
            init.read_yaml(defaults)

    @staticmethod
    def test_read_non_file() -> None:
        """Check that reading a non existing file gives an empty dictionary."""
        data = init.read_yaml(pathlib.Path())
        assert isinstance(data, dict), "read_yaml must return a dictionary."
        assert not data, "the dictionary is not empty"


class TestAutocompletion:  # pylint: disable=too-few-public-methods
    """Test the init command."""

    @staticmethod
    def test_autocomplete(
        *,
        autocomplete_dir_yaml: YAMLAutocomplete,
    ) -> None:
        """Test yaml autocompletion."""
        assert set(
            init.autocomplete_yaml_file(
                None,
                None,
                incomplete=str(autocomplete_dir_yaml["path"].resolve()),
            ),
        ) == set(
            autocomplete_dir_yaml["yaml_files"],
        ), "Invalid autocompletion."

        assert set(
            init.autocomplete_yaml_file(
                None,
                None,
                incomplete=str(
                    autocomplete_dir_yaml["path"].resolve() / "test",
                ),
            ),
        ) == set(
            autocomplete_dir_yaml["yaml_files"],
        ), "Invalid autocompletion."

    @staticmethod
    def test_autocomplete_with_suffix(
        *,
        autocomplete_dir_yaml: YAMLAutocomplete,
    ) -> None:
        """Test yaml autocompletion."""
        assert set(
            init.autocomplete_yaml_file(
                None,
                None,
                incomplete=str(
                    autocomplete_dir_yaml["path"].resolve() / "test.y",
                ),
            ),
        ) == set(
            autocomplete_dir_yaml["yaml_files"],
        ), "Invalid autocompletion."

        assert (
            set(
                init.autocomplete_yaml_file(
                    None,
                    None,
                    incomplete=str(
                        autocomplete_dir_yaml["path"].resolve() / "test.t",
                    ),
                ),
            )
            == set()
        ), "Invalid autocompletion."

    @staticmethod
    def test_autocomplete_full(
        *,
        autocomplete_dir_yaml: YAMLAutocomplete,
    ) -> None:
        """Test yaml autocompletion."""
        assert set(
            init.autocomplete_yaml_file(
                None,
                None,
                incomplete=str(
                    autocomplete_dir_yaml["path"].resolve() / "test.yaml",
                ),
            ),
        ) == {"test.yaml"}, "Invalid autocompletion."
