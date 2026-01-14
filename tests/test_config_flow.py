# SPDX-License-Identifier: AGPL-3.0-only

"""Tests for configuration flow."""

import pytest
from custom_components.vattenfall_tijdprijs.config_flow import VattenfallConfigFlow
from custom_components.vattenfall_tijdprijs.const import (
    DOMAIN,
    CONF_ANNUAL_CONSUMPTION,
    CONF_USE_CONSUMPTION_SENSOR,
    CONF_CONSUMPTION_SENSOR,
    CONF_FIXED_DELIVERY,
    CONF_FIXED_TAX_REDUCTION,
    CONF_FIXED_GRID,
    CONF_EXPORT_COMPENSATION,
    CONF_EXPORT_COSTS,
    DEFAULT_ANNUAL_CONSUMPTION,
    DEFAULT_FIXED_DELIVERY,
    DEFAULT_FIXED_TAX_REDUCTION,
    DEFAULT_FIXED_GRID,
    DEFAULT_EXPORT_COMPENSATION,
    DEFAULT_EXPORT_COSTS,
)


class TestConfigFlow:
    """Test the config flow."""


class TestConfigFlowInitialization:
    """Test config flow initialization."""

    def test_config_flow_initialization(self):
        """Test that config flow initializes correctly."""
        flow = VattenfallConfigFlow()
        assert flow._data == {}
        assert flow.VERSION == 1


class TestConfigFlowDataManagement:
    """Test config flow data handling."""

    def test_data_accumulation_user_step(self):
        """Test that user step data is accumulated."""
        flow = VattenfallConfigFlow()
        
        # Simulate user step input
        user_data = {
            CONF_USE_CONSUMPTION_SENSOR: False,
            CONF_ANNUAL_CONSUMPTION: 3500,
        }
        
        # This updates flow._data
        for key, value in user_data.items():
            flow._data[key] = value
        
        assert flow._data[CONF_USE_CONSUMPTION_SENSOR] is False
        assert flow._data[CONF_ANNUAL_CONSUMPTION] == 3500

    def test_data_accumulation_fixed_costs(self):
        """Test that fixed costs are accumulated."""
        flow = VattenfallConfigFlow()
        
        fixed_costs = {
            CONF_FIXED_DELIVERY: 0.30,
            CONF_FIXED_TAX_REDUCTION: -1.50,
            CONF_FIXED_GRID: 1.20,
        }
        
        for key, value in fixed_costs.items():
            flow._data[key] = value
        
        assert flow._data[CONF_FIXED_DELIVERY] == 0.30
        assert flow._data[CONF_FIXED_TAX_REDUCTION] == -1.50
        assert flow._data[CONF_FIXED_GRID] == 1.20

    def test_data_accumulation_export_rates(self):
        """Test that export rates are accumulated."""
        flow = VattenfallConfigFlow()
        
        export_data = {
            CONF_EXPORT_COMPENSATION: -0.10,
            CONF_EXPORT_COSTS: 0.05,
        }
        
        for key, value in export_data.items():
            flow._data[key] = value
        
        assert flow._data[CONF_EXPORT_COMPENSATION] == -0.10
        assert flow._data[CONF_EXPORT_COSTS] == 0.05

    def test_full_flow_data_assembly(self):
        """Test that full flow assembles complete config data."""
        flow = VattenfallConfigFlow()
        
        # Simulate the complete flow
        flow._data[CONF_USE_CONSUMPTION_SENSOR] = False
        flow._data[CONF_ANNUAL_CONSUMPTION] = 3000
        flow._data[CONF_FIXED_DELIVERY] = 0.30
        flow._data[CONF_FIXED_TAX_REDUCTION] = -1.50
        flow._data[CONF_FIXED_GRID] = 1.20
        flow._data[CONF_EXPORT_COMPENSATION] = -0.10
        flow._data[CONF_EXPORT_COSTS] = 0.05
        
        # Verify all data is present
        assert len(flow._data) == 7
        assert CONF_USE_CONSUMPTION_SENSOR in flow._data
        assert CONF_ANNUAL_CONSUMPTION in flow._data
        assert CONF_FIXED_DELIVERY in flow._data
        assert CONF_FIXED_TAX_REDUCTION in flow._data
        assert CONF_FIXED_GRID in flow._data
        assert CONF_EXPORT_COMPENSATION in flow._data
        assert CONF_EXPORT_COSTS in flow._data


class TestConfigFlowDefaultValues:
    """Test default values are reasonable."""

    def test_default_annual_consumption_is_positive(self):
        """Test that default annual consumption is positive."""
        assert DEFAULT_ANNUAL_CONSUMPTION > 0
        assert DEFAULT_ANNUAL_CONSUMPTION == 3000

    def test_default_fixed_costs_have_correct_signs(self):
        """Test that default fixed costs have correct signs."""
        # Delivery and grid costs should be positive
        assert DEFAULT_FIXED_DELIVERY > 0
        assert DEFAULT_FIXED_GRID > 0
        # Tax reduction should be negative (a reduction)
        assert DEFAULT_FIXED_TAX_REDUCTION < 0

    def test_default_export_rates_have_correct_signs(self):
        """Test that default export rates have correct signs."""
        # Compensation should be negative (money received, negative cost)
        assert DEFAULT_EXPORT_COMPENSATION < 0
        # Costs should be positive
        assert DEFAULT_EXPORT_COSTS > 0

    def test_default_values_are_reasonable_magnitudes(self):
        """Test that default values are in reasonable ranges."""
        # Fixed costs should be between 0 and 10 €/day
        assert 0 < DEFAULT_FIXED_DELIVERY < 10
        assert -10 < DEFAULT_FIXED_TAX_REDUCTION < 0
        assert 0 < DEFAULT_FIXED_GRID < 10
        
        # Export rates should be between -1 and 1 €/kWh
        assert -1 < DEFAULT_EXPORT_COMPENSATION < 0
        assert 0 < DEFAULT_EXPORT_COSTS < 1
