{% include "jinja_template/license_header.py.j2" %}
"""Discover the package's version number."""

from importlib import metadata


__version__ = metadata.version(__package__)
"""The package version number as found by importlib metadata."""
