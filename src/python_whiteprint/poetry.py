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
    """Poetry CLI is not found on the system."""


class LockingFailedError(RuntimeError):
    """Poetry lock failed."""


def lock(
    destination: Path,
    *,
    quiet: bool = True,
    no_cache: bool = True,
) -> None:
    """Run poetry lock.

    Args:
        destination: the path of the Poetry repository (directory containing
            the file named `pyproject.toml`).
        quiet: if True run the locking process in quiet mode otherwise run in
            verbose mode.
        no_cache: disable cache for locking.
    """
    if (poetry := shutil.which("poetry")) is None:  # pragma: no cover
        # We do not cover the case where the Poetry CLI is not found as it is a
        # requirement of the project
        raise PoetryNotFoundError

    command = [poetry, "lock", "--no-interaction"]

    # We ignore covering the --quiet and --no-cache flags **yet** as it is
    # difficult to test for little benefits. These flags are not supposed
    # to change the behavious of poetry lock.
    if no_cache:  # pragma: no cover
        command += ["--no-cache"]

    if quiet:  # pragma: no cover
        command += ["--quiet"]
    else:  # pragma: no cover
        command += ["--verbose"] * 3

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


def robust_lock(
    destination: Path,
    *,
    quiet: bool = True,
    retry: int = 3,
) -> None:
    """Run poetry lock with retry on failure.

    Note:
        cache is disable after first locking failure.

    Args:
        destination: the path of the Poetry repository (directory containing
            the file named `pyproject.toml`).
        quiet: if True run the locking process in quiet mode otherwise run in
            verbose mode.
        retry: number of retry on failure.
    """
    for i in range(retry):
        try:
            lock(destination, quiet=quiet, no_cache=i > 0)
        except (
            subprocess.CalledProcessError
        ) as called_process_error:  # pragma: no cover
            # We ignore covering the lock fail case **yet** as it is difficult
            # to test for little benefits.
            logger = logging.getLogger(__name__)
            logger.debug(
                "Completed process: '%s' with return code %d. Captured stdout:"
                " %s. Captured stderr: %s",
                called_process_error.cmd,
                called_process_error.returncode,
                called_process_error.stdout,
                called_process_error.stderr,
            )
        else:  # pragma: no cover
            return

    raise LockingFailedError  # pragma: no cover
