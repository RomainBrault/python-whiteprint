# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Git related functionalities."""

import contextlib
import os
import pathlib

from beartype import beartype
from beartype.typing import Generator, List
from nox import _options, tasks, workflow

from python_whiteprint.loc import _


_NOX_SIGINT_EXIT = 130
"""Nox return code when a SIGINT (ctl+c) is captured."""

_NOX_SUCCESS = 0
"""Nox success return code."""


@beartype
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


@beartype
def run(destination: pathlib.Path, *, args: List[str]) -> None:
    """Run a Nox command.

    Args:
        destination: the path of the Nox repository (directory containing a
            file named `noxfile.py`).
        args: a list of arguments passed to the nox command.

    Raises:
        NoxError: nox return code is not 0 (_NOX_SUCCESS).
        KeyboardInterrupt: nox return code is 130.
    """
    options = _options.options
    parser = options.parser()
    nox_args = parser.parse_args(args)
    options._finalize_args(nox_args)  # pylint: disable=protected-access

    with working_directory(destination):
        exit_code = workflow.execute(
            global_config=nox_args,
            workflow=(
                tasks.load_nox_module,
                tasks.merge_noxfile_options,
                tasks.discover_manifest,
                tasks.filter_manifest,
                tasks.honor_list_request,
                tasks.run_manifest,
                tasks.print_summary,
                tasks.create_report,
                tasks.final_reduce,
            ),
        )

    if exit_code == _NOX_SIGINT_EXIT:  # pragma: no cover
        # We ignore covering the SIGINT case **yet** as it is difficult to test
        # for little benefits.
        # To test this case, we need to run the function in a different
        # process, find the pid and eventualy kill this pid. Also note that
        # multiprocess coverage is non trivial and might require changes in
        # coverage's configuration.
        raise KeyboardInterrupt

    if exit_code != _NOX_SUCCESS:
        raise NoxError(exit_code)
