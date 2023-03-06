# SPDX-FileCopyrightText: 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""An example module."""
from beartype import beartype

from python_whiteprint import console


@beartype
def hello_world() -> None:
    """Print 'Hello, World!' to the standard output.

    Example:
        >>> hello_world()
        Hello, World!
    """
    console.DEFAULT.print("Hello, World!")
