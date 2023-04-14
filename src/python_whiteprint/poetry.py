# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Poetry."""

import logging
import pathlib
import shutil
import subprocess  # nosec

from beartype import beartype

from python_whiteprint import filesystem


@beartype
class PoetryNotFoundError(RuntimeError):
    """poetry CLI is not found on the system."""


@beartype
def lock(destination: pathlib.Path) -> None:
    """Run poetry lock.

    Args:
        destination: the path of the Poetry repository (directory containing
            the file named `pyproject.toml`).
    """
    if (poetry := shutil.which("poetry")) is None:  # pragma: no cover
        # We do not cover the case where the Poetry CLI is not found as it is a
        # requirement of the project
        raise PoetryNotFoundError

    command = [poetry, "lock"]
    logger = logging.getLogger(__name__)
    logger.debug("Running command: '%s'", " ".join(command))
    with filesystem.working_directory(destination):
        subprocess.run(  # nosec
            command,
            shell=False,
            check=True,
        )
