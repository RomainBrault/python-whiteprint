# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Poetry."""

import pathlib

from beartype import beartype
from cleo.io import null_io
from poetry import factory
from poetry.installation import installer
from poetry.utils import env


@beartype
def lock(destination: pathlib.Path) -> None:
    """Run poetry lock.

    Args:
        destination: the path of the Poetry repository (directory containing
            the file named `pyproject.toml`).
    """
    poetry = factory.Factory().create_poetry(destination)
    console_io = null_io.NullIO()
    poetry_installer = installer.Installer(
        console_io,
        env.EnvManager(poetry).create_venv(),
        poetry.package,
        poetry.locker,
        poetry.pool,
        poetry.config,
    )
    poetry_installer.lock(update=False)
    poetry_installer.run()
