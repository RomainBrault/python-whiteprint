{% include "jinja_template/license_header.py.j2" %}
"""Localization."""

import gettext
import pathlib


LOCALE_DIRECTORY = pathlib.Path(__file__).parent / "locale"
TRANSLATION = gettext.translation(
    "messages",
    LOCALE_DIRECTORY,
    fallback=True,
)
_ = TRANSLATION.gettext
"""Convenient access to gettext."""
