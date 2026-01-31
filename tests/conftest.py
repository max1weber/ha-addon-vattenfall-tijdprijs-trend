# SPDX-License-Identifier: AGPL-3.0-only

"""Pytest configuration and fixtures."""

import sys
from unittest.mock import MagicMock

import pytest


# Create real base classes for mocked Home Assistant entities
class MockSensorEntity:
    """Mock SensorEntity base class."""
    _attr_name = None
    _attr_native_value = None
    _attr_native_unit_of_measurement = None
    _attr_device_class = None
    _attr_icon = None
    _attr_unique_id = None
    _attr_extra_state_attributes = {}
    
    def __init__(self):
        pass


class MockConfigFlow:
    """Mock ConfigFlow base class."""
    VERSION = 1
    
    def __init_subclass__(cls, domain=None, **kwargs):
        """Allow subclassing with domain parameter."""
        super().__init_subclass__(**kwargs)
        cls.domain = domain
    
    async def async_step_user(self, user_input=None):
        pass
    
    async def async_step_init(self, user_input=None):
        pass
    
    def async_create_entry(self, title, data):
        return {"version": self.VERSION, "title": title, "data": data}


# Mock homeassistant modules before any test imports
homeassistant_mock = MagicMock()
homeassistant_mock.__path__ = []

config_entries_mock = MagicMock()
config_entries_mock.ConfigFlow = MockConfigFlow
homeassistant_mock.config_entries = config_entries_mock

core_mock = MagicMock()
core_mock.callback = lambda x: x  # Identity decorator
homeassistant_mock.core = core_mock

helpers_mock = MagicMock()
helpers_mock.__path__ = []
homeassistant_mock.helpers = helpers_mock

config_validation_mock = MagicMock()
helpers_mock.config_validation = config_validation_mock

selector_mock = MagicMock()
selector_mock.EntitySelector = MagicMock
selector_mock.EntitySelectorConfig = MagicMock
selector_mock.NumberSelector = MagicMock
selector_mock.NumberSelectorConfig = MagicMock
helpers_mock.selector = selector_mock

components_mock = MagicMock()
components_mock.__path__ = []
homeassistant_mock.components = components_mock

sensor_mock = MagicMock()
sensor_mock.SensorEntity = MockSensorEntity
components_mock.sensor = sensor_mock

const_mock = MagicMock()
const_mock.Platform = MagicMock()
homeassistant_mock.const = const_mock

util_mock = MagicMock()
util_mock.dt = MagicMock()
homeassistant_mock.util = util_mock

sys.modules['homeassistant'] = homeassistant_mock
sys.modules['homeassistant.config_entries'] = config_entries_mock
sys.modules['homeassistant.core'] = core_mock
sys.modules['homeassistant.helpers'] = helpers_mock
sys.modules['homeassistant.helpers.config_validation'] = config_validation_mock
sys.modules['homeassistant.helpers.selector'] = selector_mock
sys.modules['homeassistant.components'] = components_mock
sys.modules['homeassistant.components.sensor'] = sensor_mock
sys.modules['homeassistant.const'] = const_mock
sys.modules['homeassistant.util'] = util_mock


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
