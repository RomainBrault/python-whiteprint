{% include "jinja_template/license_header.py.j2" %}
"""Test the main CLI."""

from beartype import beartype
from typer import testing

from {{package_name}} import version
from {{package_name}}.cli import entrypoint


@beartype
class TestCLI:
    """Test the CLI."""

    @staticmethod
    def test_version(cli_runner: testing.CliRunner) -> None:
        """Check if the version printed by the CLI match the API one."""
        result = cli_runner.invoke(
            entrypoint.app,
            ["--version"],
        )
        assert result.exit_code == 0, "The CLI did not exit properly."
        assert version.__version__ == result.stdout.rstrip(), (
            "The python version returned by the CLI do not match the API"
            " version (given by __version__)."
        )

    @staticmethod
    def test_help_flag_exists(cli_runner: testing.CliRunner) -> None:
        """Check if the version printed by the CLI match the API one."""
        result = cli_runner.invoke(
            entrypoint.app,
            ["--help"],
        )
        assert result.exit_code == 0, "The CLI did not exit properly."

    @staticmethod
    def test_default(cli_runner: testing.CliRunner) -> None:
        """Check if the CLI called with default arguments return prpperly.

        Args:
            cli_runner: the CLI test runner provided by typer.testing or a
                fixture.
        """
        result = cli_runner.invoke(entrypoint.app)
        assert result.exit_code == 0, "The CLI did not exit properly."
