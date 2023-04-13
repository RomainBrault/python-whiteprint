#!/usr/bin/env python
{% include "jinja_template/license_header.py.j2" %}
"""Top-level executable."""

from {{package_name}}.cli import entrypoint


entrypoint.app()
