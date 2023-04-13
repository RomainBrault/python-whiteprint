# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Discover the package's version number."""

from importlib import metadata


__version__ = metadata.version(__package__)
"""The package version number as found by importlib metadata."""
