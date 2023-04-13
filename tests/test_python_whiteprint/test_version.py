# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Test the version module."""

import re

from beartype import beartype

from python_whiteprint import version


@beartype
class TestVersion:
    """Test the __version__ variable."""

    @staticmethod
    def is_canonical(version_number: str) -> bool:
        """Determine if version number is well formed.

        Version numbers must respect PEP440
        """
        pep_440 = (
            r"^([1-9][0-9]*!)"
            r"?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))"
            r"?(\.post(0|[1-9][0-9]*))"
            r"?(\.dev(0|[1-9][0-9]*))?$"
        )
        return re.match(pep_440, version_number) is not None

    @staticmethod
    def test___version___respects_pep_440() -> None:
        """Test the version number is well formed.

        Version numbers must respect PEP440
        """
        assert TestVersion.is_canonical(
            version.__version__,
        ), f"The version number {version.__version__} does not respect PEP440."
