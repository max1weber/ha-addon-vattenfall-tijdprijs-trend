# SPDX-License-Identifier: AGPL-3.0-only

"""Tests for sensor entities."""

import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch, AsyncMock

from custom_components.vattenfall_tijdprijs.sensor import (
    async_setup_entry,
    PriceSensor,
    FixedCostSensor,
    CurrentPriceSensor,
    HourlyPriceSensor,
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


class TestCurrentPriceSensor:
    """Test CurrentPriceSensor entity."""
    
    def test_current_price_sensor_initialization(self):
        """Test CurrentPriceSensor initializes correctly."""
        config_data = {}
        entry_id = "test_entry_123"
        sensor = CurrentPriceSensor(config_data, entry_id, "Test Current Price", "import_price")
        
        assert sensor._attr_name == "Test Current Price"
        assert sensor._attr_native_unit_of_measurement == DEFAULT_UNIT_PRICE
        assert sensor._attr_icon == "mdi:currency-eur"
        assert sensor._attr_unique_id == "test_entry_123_import_price"
    
    @patch('custom_components.vattenfall_tijdprijs.sensor.datetime')
    def test_current_price_value(self, mock_datetime):
        """Test that current price is calculated correctly."""
        mock_datetime.now.return_value = datetime(2024, 6, 10, 14, 0)  # Summer weekday 14:00
        
        config_data = {}
        entry_id = "test_entry_123"
        sensor = CurrentPriceSensor(config_data, entry_id, "Test", "import_price")
        
        price = sensor.native_value
        assert isinstance(price, float)
        assert price > 0
    
    @patch('custom_components.vattenfall_tijdprijs.sensor.datetime')
    def test_current_price_attributes(self, mock_datetime):
        """Test extra state attributes."""
        mock_datetime.now.return_value = datetime(2024, 6, 10, 14, 0)
        
        config_data = {}
        entry_id = "test_entry_123"
        sensor = CurrentPriceSensor(config_data, entry_id, "Test", "import_price")
        
        attrs = sensor.extra_state_attributes
        assert "season" in attrs
        assert "period" in attrs
        assert "hour" in attrs
        assert attrs["season"] == "summer"
        assert attrs["hour"] == 14


class TestHourlyPriceSensor:
    """Test HourlyPriceSensor entity."""
    
    def test_hourly_price_sensor_initialization(self):
        """Test HourlyPriceSensor initializes correctly."""
        config_data = {}
        entry_id = "test_entry_123"
        sensor = HourlyPriceSensor(config_data, entry_id, "Test Hourly Prices", "hourly_prices")
        
        assert sensor._attr_name == "Test Hourly Prices"
        assert sensor._attr_native_unit_of_measurement == DEFAULT_UNIT_PRICE
        assert sensor._attr_icon == "mdi:chart-line"
        assert sensor._attr_unique_id == "test_entry_123_hourly_prices"
    
    @patch('custom_components.vattenfall_tijdprijs.sensor.datetime')
    def test_hourly_price_attributes(self, mock_datetime):
        """Test that hourly prices are in attributes."""
        mock_datetime.now.return_value = datetime(2024, 6, 10, 14, 0)
        
        config_data = {}
        entry_id = "test_entry_123"
        sensor = HourlyPriceSensor(config_data, entry_id, "Test", "hourly_prices")
        
        attrs = sensor.extra_state_attributes
        assert "hourly_prices" in attrs
        assert "forecast_hours" in attrs
        assert "last_update" in attrs
        assert "apexcharts_data" in attrs
        assert "median_price" in attrs
        assert len(attrs["hourly_prices"]) == 48
        assert len(attrs["apexcharts_data"]) == 48
        assert attrs["forecast_hours"] == 48
    
    @patch('custom_components.vattenfall_tijdprijs.sensor.datetime')
    def test_hourly_prices_structure(self, mock_datetime):
        """Test structure of hourly price data."""
        mock_datetime.now.return_value = datetime(2024, 6, 10, 14, 0)
        
        config_data = {}
        entry_id = "test_entry_123"
        sensor = HourlyPriceSensor(config_data, entry_id, "Test", "hourly_prices")
        
        hourly_prices = sensor.extra_state_attributes["hourly_prices"]
        first_hour = hourly_prices[0]
        
        assert "time" in first_hour
        assert "hour" in first_hour
        assert "price" in first_hour
        assert "period" in first_hour
        assert "season" in first_hour
        
        # Test ApexCharts data format with color coding
        apexcharts_data = sensor.extra_state_attributes["apexcharts_data"]
        first_chart_entry = apexcharts_data[0]
        
        assert "x" in first_chart_entry
        assert "y" in first_chart_entry
        assert "fillColor" in first_chart_entry
        assert isinstance(first_chart_entry["y"], float)
        assert first_chart_entry["fillColor"] in ["#27ae60", "#e74c3c"]  # Green or red
        
        # Verify all entries have colors
        for entry in apexcharts_data:
            assert entry["fillColor"] in ["#27ae60", "#e74c3c"]
        
        # Verify median_price is present and reasonable
        median_price = sensor.extra_state_attributes["median_price"]
        assert isinstance(median_price, float)
        assert median_price > 0


class TestPriceSensor:
    """Test PriceSensor entity."""

    def test_price_sensor_initialization(self):
        """Test PriceSensor initializes with correct attributes."""
        entry_id = "test_entry_123"
        sensor = PriceSensor(entry_id, "Import prijs", 0.25, DEFAULT_UNIT_PRICE, "import_test")
        
        assert sensor._attr_name == "Import prijs"
        assert sensor._attr_native_value == 0.25
        assert sensor._attr_native_unit_of_measurement == DEFAULT_UNIT_PRICE
        assert sensor._attr_unique_id == "test_entry_123_import_test"

    def test_price_sensor_different_values(self):
        """Test PriceSensor with different price values."""
        entry_id = "test_entry_123"
        prices = [0.10, 0.15, 0.25, 0.50, 0.75]
        
        for i, price in enumerate(prices):
            sensor = PriceSensor(entry_id, "Test Price", price, DEFAULT_UNIT_PRICE, f"test_{i}")
            assert sensor._attr_native_value == price

    def test_price_sensor_zero_value(self):
        """Test PriceSensor with zero price."""
        entry_id = "test_entry_123"
        sensor = PriceSensor(entry_id, "Free period", 0.0, DEFAULT_UNIT_PRICE, "zero_price")
        
        assert sensor._attr_native_value == 0.0

    def test_price_sensor_negative_value(self):
        """Test PriceSensor with negative price (subsidy)."""
        entry_id = "test_entry_123"
        sensor = PriceSensor(entry_id, "Export compensation", -0.05, DEFAULT_UNIT_PRICE, "export_comp")
        
        assert sensor._attr_native_value == -0.05

    def test_price_sensor_unit(self):
        """Test PriceSensor has correct unit."""
        entry_id = "test_entry_123"
        sensor = PriceSensor(entry_id, "Price", 0.20, DEFAULT_UNIT_PRICE, "price_unit")
        
        assert sensor._attr_native_unit_of_measurement == "€/kWh"


class TestFixedCostSensor:
    """Test FixedCostSensor entity."""

    def test_fixed_cost_sensor_initialization(self):
        """Test FixedCostSensor initializes with correct attributes."""
        entry_id = "test_entry_123"
        sensor = FixedCostSensor(entry_id, "Vaste leveringskosten", 0.30, "fixed_delivery")
        
        assert sensor._attr_name == "Vaste leveringskosten"
        assert sensor._attr_native_value == 0.30
        assert sensor._attr_native_unit_of_measurement == DEFAULT_UNIT_FIXED
        assert sensor._attr_unique_id == "test_entry_123_fixed_delivery"

    def test_fixed_cost_sensor_different_values(self):
        """Test FixedCostSensor with different cost values."""
        entry_id = "test_entry_123"
        costs = [0.15, 0.50, 1.00, 2.50]
        
        for i, cost in enumerate(costs):
            sensor = FixedCostSensor(entry_id, "Test Cost", cost, f"cost_{i}")
            assert sensor._attr_native_value == cost

    def test_fixed_cost_sensor_negative_value(self):
        """Test FixedCostSensor with negative cost (reduction)."""
        entry_id = "test_entry_123"
        sensor = FixedCostSensor(entry_id, "Tax reduction", -1.50, "tax_reduction")
        
        assert sensor._attr_native_value == -1.50

    def test_fixed_cost_sensor_unit(self):
        """Test FixedCostSensor has correct unit."""
        entry_id = "test_entry_123"
        sensor = FixedCostSensor(entry_id, "Fixed cost", 0.50, "fixed_cost")
        
        assert sensor._attr_native_unit_of_measurement == "€/dag"


class TestAsyncSetupEntry:
    """Test async_setup_entry function."""

    async def test_setup_entry_creates_all_sensors(self):
        """Test that setup_entry creates all expected sensors."""
        hass = MagicMock()
        entry = MagicMock()
        entry.entry_id = "test_entry_123"
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
        
        # Should have 7 sensors (2 dynamic + 2 export + 3 fixed cost)
        assert len(added_entities) == 7

    async def test_setup_entry_sensor_names(self):
        """Test that setup_entry creates sensors with correct names."""
        hass = MagicMock()
        entry = MagicMock()
        entry.entry_id = "test_entry_123"
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
        
        assert "Huidige Importprijs" in sensor_names
        assert "Importprijs per uur" in sensor_names
        assert "Terugleververgoeding" in sensor_names
        assert "Terugleverkosten" in sensor_names
        assert "Vaste leveringskosten" in sensor_names
        assert "Vaste belastingvermindering" in sensor_names
        assert "Vaste netbeheerkosten" in sensor_names

    async def test_setup_entry_sensor_values(self):
        """Test that setup_entry creates sensors with correct values."""
        hass = MagicMock()
        entry = MagicMock()
        entry.entry_id = "test_entry_123"
        
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
        
        # Find static sensors by name and check their values
        static_sensors = [s for s in added_entities if hasattr(s, '_attr_native_value') and not callable(getattr(s, 'native_value', None))]
        sensor_values = {sensor._attr_name: sensor._attr_native_value for sensor in static_sensors}
        
        assert sensor_values["Terugleververgoeding"] == 0.15
        assert sensor_values["Terugleverkosten"] == 0.08
        assert sensor_values["Vaste leveringskosten"] == 0.45
        assert sensor_values["Vaste netbeheerkosten"] == 1.50
        assert sensor_values["Vaste belastingvermindering"] == -1.80


class TestUniqueSensorIds:
    """Test that all sensors have unique IDs."""

    async def test_all_sensors_have_unique_ids(self):
        """Test that all sensors generated by async_setup_entry have unique_id set."""
        hass = MagicMock()
        entry = MagicMock()
        entry.entry_id = "test_entry_456"
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
        
        # All sensors should have unique_id
        for sensor in added_entities:
            assert hasattr(sensor, '_attr_unique_id'), f"Sensor {sensor._attr_name} missing unique_id"
            assert sensor._attr_unique_id is not None, f"Sensor {sensor._attr_name} has None unique_id"
            assert isinstance(sensor._attr_unique_id, str), f"Sensor {sensor._attr_name} unique_id is not a string"
    
    async def test_unique_ids_are_unique(self):
        """Test that all unique_ids are different from each other."""
        hass = MagicMock()
        entry = MagicMock()
        entry.entry_id = "test_entry_789"
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
        unique_ids = [sensor._attr_unique_id for sensor in added_entities]
        
        # All unique_ids should be unique
        assert len(unique_ids) == len(set(unique_ids)), "Duplicate unique_ids found"
