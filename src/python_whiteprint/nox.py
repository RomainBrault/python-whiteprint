# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Git related functionalities."""

import logging
import shutil
import subprocess  # nosec
from pathlib import Path
from typing import Final

from beartype.typing import List

from python_whiteprint import filesystem
from python_whiteprint.loc import _


__all__: Final = ["NoxNotFoundError", "NoxError", "run"]
"""Public module attributes."""


_NOX_SIGINT_EXIT: Final = 130
"""Nox return code when a SIGINT (ctl+c) is captured."""

_NOX_SUCCESS: Final = 0
"""Nox success return code."""


class NoxNotFoundError(RuntimeError):
    """poetry CLI is not found on the system."""


class NoxError(RuntimeError):
    """A Nox error occured.

    Attributes:
        exit_code: nox's exit code.

    Args:
        exit_code: nox's exit code.
    """

    def __init__(self, exit_code: int) -> None:
        """Init NoxError."""
        self.exit_code = exit_code
        super().__init__(_("Nox exit code: {}").format(self.exit_code))


def run(destination: Path, *, args: List[str]) -> None:
    """Run a Nox command.

    Args:
        destination: the path of the Nox repository (directory containing a
            file named `noxfile.py`).
        args: a list of arguments passed to the nox command.

    Raises:
        NoxError: nox return code is not 0 (_NOX_SUCCESS).
        KeyboardInterrupt: nox return code is 130.
    """
    if (nox := shutil.which("nox")) is None:  # pragma: no cover
        # We do not cover the case where the Nox CLI is not found as it is a
        # requirement of the project
        raise NoxNotFoundError

    command = [nox, *args]
    logger = logging.getLogger(__name__)
    logger.debug("Starting process: '%s'", " ".join(command))
    with filesystem.working_directory(destination):
        completed_process = subprocess.run(  # nosec
            command, shell=False, check=False
        )

    logger.debug(
        "Completed process: '%s' with return code %d. Captured stdout: %s."
        " Captured stderr: %s",
        completed_process.args,
        completed_process.returncode,
        completed_process.stdout,
        completed_process.stderr,
    )

    if (
        exit_code := completed_process.returncode
    ) == _NOX_SIGINT_EXIT:  # pragma: no cover
        # We ignore covering the SIGINT case **yet** as it is difficult to test
        # for little benefits.
        # To test this case, we need to run the function in a different
        # process, find the pid and eventualy kill this pid. Also note that
        # multiprocess coverage is non trivial and might require changes in
        # coverage's configuration.
        raise KeyboardInterrupt

    if exit_code != _NOX_SUCCESS:
        raise NoxError(exit_code)
