# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Filesystem utilities."""

import contextlib
import os
import pathlib

from beartype import beartype
from beartype.typing import Generator


@contextlib.contextmanager
@beartype
def working_directory(path: pathlib.Path) -> Generator[None, None, None]:
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
    origin = pathlib.Path().resolve()
    try:
        os.chdir(path.resolve())
        yield
    finally:
        os.chdir(origin)
