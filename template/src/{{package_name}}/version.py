{% include "jinja_template/license_header.py.j2" %}
"""Discover the package's version number."""

from importlib import metadata
from typing import Final


__all__: Final = ["__version__"]
"""Public module attributes."""

__version__ = metadata.version(__package__)
"""The package version number as found by importlib metadata."""
