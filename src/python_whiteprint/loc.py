# SPDX-FileCopyrightText: 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT
"""Localization."""

import gettext


TRANSLATION = gettext.translation("messages", "locale", fallback=True)
_ = TRANSLATION.gettext
"""Convenient access to gettext."""
