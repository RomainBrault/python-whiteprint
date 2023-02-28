"""An example module."""
import typeguard

from python_whiteprint import console


@typeguard.typechecked
def hello_world() -> None:
    """Print 'Hello, World!' to the standard output.

    Example:
        ```pycon
        >>> hello_world()
        Hello, World!

        ```
    """
    console.DEFAULT.print("Hello, World!")
