# SPDX-License-Identifier: AGPL-3.0-only

"""Pytest configuration and fixtures."""

import pytest
from unittest.mock import MagicMock


@pytest.fixture
def hass():
    """Return a mock Home Assistant instance."""
    mock_hass = MagicMock()
    mock_hass.data = {}
    return mock_hass


@pytest.fixture
def mock_config_entry():
    """Return a mock config entry."""
    entry = MagicMock()
    entry.data = {}
    entry.title = "Vattenfall Tijdprijs"
    entry.unique_id = "vattenfall_tijdprijs_test"
    return entry
