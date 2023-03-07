# SPDX-FileCopyrightText: 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT
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
