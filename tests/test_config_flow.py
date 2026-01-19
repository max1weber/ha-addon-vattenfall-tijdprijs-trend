# SPDX-License-Identifier: AGPL-3.0-only

"""Tests for configuration flow."""

import pytest
from custom_components.vattenfall_tijdprijs.config_flow import VattenfallConfigFlow
from custom_components.vattenfall_tijdprijs.const import (
    DOMAIN,
    CONF_FIXED_DELIVERY,
    CONF_FIXED_TAX_REDUCTION,
    CONF_FIXED_GRID,
    CONF_EXPORT_COMPENSATION,
    CONF_EXPORT_COSTS,
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
        assert flow.VERSION == 1


class TestConfigFlowDefaultValues:
    """Test default values are reasonable."""

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
