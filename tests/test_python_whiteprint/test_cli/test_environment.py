# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Test the CLI's environment."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from python_whiteprint.cli.environment import (
    str2bool,
)
from python_whiteprint.cli.exceptions import (
    BOOLEAN_STRING,
    NotAValidBooleanError,
)


class TestStr2Bool:
    """Test the module's utility functions."""

    @staticmethod
    @given(st.sampled_from(sorted(BOOLEAN_STRING.true)))
    def test_true_strings(string: str) -> None:
        """Test strings representing True."""
        assert str2bool(string) is True
        assert str2bool(string.upper()) is True

    @staticmethod
    @given(st.sampled_from(sorted(BOOLEAN_STRING.false)))
    def test_false_strings(string: str) -> None:
        """Test strings representing False."""
        assert str2bool(string) is False
        assert str2bool(string.upper()) is False

    @staticmethod
    @given(st.booleans())
    def test_booleans(boolean: bool) -> None:
        """Test boolean inputs."""
        assert str2bool(boolean) is boolean

    @staticmethod
    def test_invalid_string() -> None:
        """Test invalid string."""
        with pytest.raises(NotAValidBooleanError):
            str2bool("invalid_string")
