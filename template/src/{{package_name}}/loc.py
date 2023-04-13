{% include "jinja_template/license_header.py.j2" %}
"""Localization."""

import gettext
import pathlib


LOCALE_DIRECTORY = pathlib.Path(__file__).parent / "locale"
"""Path to the directory containing the locales."""

TRANSLATION = gettext.translation(
    "messages",
    LOCALE_DIRECTORY,
    fallback=True,
)
"""A Gettext translation."""

_ = TRANSLATION.gettext
"""Convenient access to gettext."""
