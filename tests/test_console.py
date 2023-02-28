"""Test the console module."""
import typeguard
from rich import console as rich_console

from python_whiteprint import console as python_whiteprint_console


@typeguard.typechecked
def test_console() -> None:
    """Check that the console is a rich console instance."""
    assert isinstance(python_whiteprint_console.DEFAULT, rich_console.Console)
