# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Top-level module."""

import logging
from typing import Final

from beartype.claw import beartype_this_package

from python_whiteprint.version import __version__


__all__: Final = ["__version__"]
"""Public module attributes."""


logging.captureWarnings(True)
beartype_this_package()
