{% include "jinja_template/license_header.py.j2" %}
"""Top-level module."""

from typing import Final

from beartype.claw import beartype_this_package

from {{package_name}}.version import __version__


__all__: Final = ["__version__"]
"""Public module attributes."""


beartype_this_package()
