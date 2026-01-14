# SPDX-License-Identifier: AGPL-3.0-only

"""Tests for sensor entities."""

import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant

from custom_components.vattenfall_tijdprijs.sensor import (
    async_setup_entry,
    PriceSensor,
    FixedCostSensor,
)
from custom_components.vattenfall_tijdprijs.const import (
    CONF_EXPORT_COMPENSATION,
    CONF_EXPORT_COSTS,
    CONF_FIXED_DELIVERY,
    CONF_FIXED_GRID,
    CONF_FIXED_TAX_REDUCTION,
    DEFAULT_UNIT_PRICE,
    DEFAULT_UNIT_FIXED,
)


class TestPriceSensor:
    """Test PriceSensor entity."""

    def test_price_sensor_initialization(self):
        """Test PriceSensor initializes with correct attributes."""
        sensor = PriceSensor("Import prijs", 0.25, DEFAULT_UNIT_PRICE)
        
        assert sensor._attr_name == "Import prijs"
        assert sensor._attr_native_value == 0.25
        assert sensor._attr_native_unit_of_measurement == DEFAULT_UNIT_PRICE

    def test_price_sensor_different_values(self):
        """Test PriceSensor with different price values."""
        prices = [0.10, 0.15, 0.25, 0.50, 0.75]
        
        for price in prices:
            sensor = PriceSensor("Test Price", price, DEFAULT_UNIT_PRICE)
            assert sensor._attr_native_value == price

    def test_price_sensor_zero_value(self):
        """Test PriceSensor with zero price."""
        sensor = PriceSensor("Free period", 0.0, DEFAULT_UNIT_PRICE)
        
        assert sensor._attr_native_value == 0.0

    def test_price_sensor_negative_value(self):
        """Test PriceSensor with negative price (subsidy)."""
        sensor = PriceSensor("Export compensation", -0.05, DEFAULT_UNIT_PRICE)
        
        assert sensor._attr_native_value == -0.05

    def test_price_sensor_unit(self):
        """Test PriceSensor has correct unit."""
        sensor = PriceSensor("Price", 0.20, DEFAULT_UNIT_PRICE)
        
        assert sensor._attr_native_unit_of_measurement == "€/kWh"


class TestFixedCostSensor:
    """Test FixedCostSensor entity."""

    def test_fixed_cost_sensor_initialization(self):
        """Test FixedCostSensor initializes with correct attributes."""
        sensor = FixedCostSensor("Vaste leveringskosten", 0.30)
        
        assert sensor._attr_name == "Vaste leveringskosten"
        assert sensor._attr_native_value == 0.30
        assert sensor._attr_native_unit_of_measurement == DEFAULT_UNIT_FIXED

    def test_fixed_cost_sensor_different_values(self):
        """Test FixedCostSensor with different cost values."""
        costs = [0.15, 0.50, 1.00, 2.50]
        
        for cost in costs:
            sensor = FixedCostSensor("Test Cost", cost)
            assert sensor._attr_native_value == cost

    def test_fixed_cost_sensor_negative_value(self):
        """Test FixedCostSensor with negative cost (reduction)."""
        sensor = FixedCostSensor("Tax reduction", -1.50)
        
        assert sensor._attr_native_value == -1.50

    def test_fixed_cost_sensor_unit(self):
        """Test FixedCostSensor has correct unit."""
        sensor = FixedCostSensor("Fixed cost", 0.50)
        
        assert sensor._attr_native_unit_of_measurement == "€/dag"


class TestAsyncSetupEntry:
    """Test async_setup_entry function."""

    async def test_setup_entry_creates_all_sensors(self):
        """Test that setup_entry creates all expected sensors."""
        hass = MagicMock(spec=HomeAssistant)
        entry = MagicMock()
        entry.data = {
            CONF_EXPORT_COMPENSATION: 0.10,
            CONF_EXPORT_COSTS: 0.05,
            CONF_FIXED_DELIVERY: 0.30,
            CONF_FIXED_GRID: 1.20,
            CONF_FIXED_TAX_REDUCTION: -1.50,
        }
        
        async_add_entities = AsyncMock()
        
        await async_setup_entry(hass, entry, async_add_entities)
        
        # Verify async_add_entities was called
        assert async_add_entities.called
        
        # Get the entities that were added
        added_entities = async_add_entities.call_args[0][0]
        
        # Should have 5 sensors (2 price sensors + 3 fixed cost sensors)
        assert len(added_entities) == 5

    async def test_setup_entry_sensor_names(self):
        """Test that setup_entry creates sensors with correct names."""
        hass = MagicMock(spec=HomeAssistant)
        entry = MagicMock()
        entry.data = {
            CONF_EXPORT_COMPENSATION: 0.10,
            CONF_EXPORT_COSTS: 0.05,
            CONF_FIXED_DELIVERY: 0.30,
            CONF_FIXED_GRID: 1.20,
            CONF_FIXED_TAX_REDUCTION: -1.50,
        }
        
        async_add_entities = AsyncMock()
        
        await async_setup_entry(hass, entry, async_add_entities)
        
        added_entities = async_add_entities.call_args[0][0]
        sensor_names = [sensor._attr_name for sensor in added_entities]
        
        assert "Terugleververgoeding" in sensor_names
        assert "Terugleverkosten" in sensor_names
        assert "Vaste leveringskosten" in sensor_names
        assert "Vaste belastingvermindering" in sensor_names
        assert "Vaste netbeheerkosten" in sensor_names

    async def test_setup_entry_sensor_values(self):
        """Test that setup_entry creates sensors with correct values."""
        hass = MagicMock(spec=HomeAssistant)
        entry = MagicMock()
        
        test_values = {
            CONF_EXPORT_COMPENSATION: 0.15,
            CONF_EXPORT_COSTS: 0.08,
            CONF_FIXED_DELIVERY: 0.45,
            CONF_FIXED_GRID: 1.50,
            CONF_FIXED_TAX_REDUCTION: -1.80,
        }
        entry.data = test_values
        
        async_add_entities = AsyncMock()
        
        await async_setup_entry(hass, entry, async_add_entities)
        
        added_entities = async_add_entities.call_args[0][0]
        
        # Find sensors by name and check their values
        sensor_values = {sensor._attr_name: sensor._attr_native_value for sensor in added_entities}
        
        assert sensor_values["Terugleververgoeding"] == 0.15
        assert sensor_values["Terugleverkosten"] == 0.08
        assert sensor_values["Vaste leveringskosten"] == 0.45
        assert sensor_values["Vaste netbeheerkosten"] == 1.50
        assert sensor_values["Vaste belastingvermindering"] == -1.80
