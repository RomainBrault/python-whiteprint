# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Filesystem utilities."""

import contextlib
import os
from pathlib import Path
from typing import Final

from beartype.typing import Generator, no_type_check


__all__: Final = ["working_directory"]
"""Public module attributes."""


# TODO: remove @no_type_check when Python 3.10 reach EOL.
# See https://github.com/beartype/beartype/issues/249.
@no_type_check
@contextlib.contextmanager
def working_directory(path: Path) -> Generator[None, None, None]:
    """Sets the current working directory (cwd) within the context.

    Args:
        path (Path): The path to the cwd

    Yields:
        None
    """
    # It is important to resolve the current directory before using chdir,
    # after the chdir function is called, the information about the current
    # directory is definitively lost, hence the absolute path of the current
    # directory must be known before.
    origin = Path().resolve()
    try:
        os.chdir(path.resolve())
        yield
    finally:
        os.chdir(origin)
