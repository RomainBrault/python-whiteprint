# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Poetry."""

import logging
import shutil
import subprocess  # nosec
from pathlib import Path
from typing import Final

from python_whiteprint import filesystem


__all__: Final = ["PoetryNotFoundError", "lock"]
"""Public module attributes."""


class PoetryNotFoundError(RuntimeError):
    """poetry CLI is not found on the system."""


def lock(destination: Path) -> None:
    """Run poetry lock.

    Args:
        destination: the path of the Poetry repository (directory containing
            the file named `pyproject.toml`).
    """
    if (poetry := shutil.which("poetry")) is None:  # pragma: no cover
        # We do not cover the case where the Poetry CLI is not found as it is a
        # requirement of the project
        raise PoetryNotFoundError

    command = [poetry, "lock", "--no-interaction"]
    logger = logging.getLogger(__name__)
    logger.debug("Starting process: '%s'", " ".join(command))
    with filesystem.working_directory(destination):
        completed_process = subprocess.run(  # nosec
            command,
            shell=False,
            check=True,
        )

    logger.debug(
        "Completed process: '%s' with return code %d. Captured stdout: %s."
        " Captured stderr: %s",
        completed_process.args,
        completed_process.returncode,
        completed_process.stdout,
        completed_process.stderr,
    )
