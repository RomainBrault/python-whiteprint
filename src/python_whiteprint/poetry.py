# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Poetry."""

import pathlib
import shutil
import subprocess  # nosec

from beartype import beartype

from python_whiteprint import filesystem


@beartype
class PoetryNotFound(RuntimeError):
    """poetry CLI is not found on the system."""


@beartype
def lock(destination: pathlib.Path) -> None:
    """Run poetry lock.

    Args:
        destination: the path of the Poetry repository (directory containing
            the file named `pyproject.toml`).
    """
    if (poetry := shutil.which("poetry")) is None:
        raise PoetryNotFound

    with filesystem.working_directory(destination):
        subprocess.run(  # nosec
            [poetry, "lock", "--no-updates"],
            shell=False,
            check=True,
        )
