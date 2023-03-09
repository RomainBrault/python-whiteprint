{% include "jinja_template/license_header.py.j2" %}
"""An example module."""
from beartype import beartype
from {{package_name}} import console
from {{package_name}}.loc import _


@beartype
def hello_world() -> None:
    """Print 'Hello, World!' to the standard output.

    Example:
        >>> hello_world()
        Hello, World!
    """
    console.DEFAULT.print(_("Hello, World!"))
