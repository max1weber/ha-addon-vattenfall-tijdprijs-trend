# SPDX-License-Identifier: AGPL-3.0-only

"""Tests for pricing data calculations."""

import pytest
from custom_components.vattenfall_tijdprijs.pricing_data import (
    get_tier_index,
    get_import_price,
    BELASTING_PER_TIER,
    DEFAULT_LEVERING_PRICES,
)


class TestGetTierIndex:
    """Test tier index calculation based on annual consumption."""

    def test_tier_0_under_2900(self):
        """Test tier 0 for consumption under 2900 kWh/year."""
        assert get_tier_index(0) == 0
        assert get_tier_index(1000) == 0
        assert get_tier_index(2899) == 0

    def test_tier_1_2900_to_9999(self):
        """Test tier 1 for consumption 2900-9999 kWh/year."""
        assert get_tier_index(2900) == 1
        assert get_tier_index(5000) == 1
        assert get_tier_index(9999) == 1

    def test_tier_2_10000_to_49999(self):
        """Test tier 2 for consumption 10000-49999 kWh/year."""
        assert get_tier_index(10000) == 2
        assert get_tier_index(25000) == 2
        assert get_tier_index(49999) == 2

    def test_tier_3_50000_and_above(self):
        """Test tier 3 for consumption 50000+ kWh/year."""
        assert get_tier_index(50000) == 3
        assert get_tier_index(100000) == 3
        assert get_tier_index(999999) == 3

    def test_boundary_values(self):
        """Test boundary values between tiers."""
        assert get_tier_index(2899.99) == 0
        assert get_tier_index(2900) == 1
        assert get_tier_index(9999.99) == 1
        assert get_tier_index(10000) == 2
        assert get_tier_index(49999.99) == 2
        assert get_tier_index(50000) == 3


class TestGetImportPrice:
    """Test import price calculation with default values."""

    def test_default_summer_normal_all_tiers(self):
        """Test default summer normal prices for all tiers."""
        for tier in range(4):
            price = get_import_price({}, "summer", "normal", tier)
            expected = DEFAULT_LEVERING_PRICES["summer_normal"][tier] + BELASTING_PER_TIER[tier]
            assert abs(price - expected) < 0.000001

    def test_default_winter_normal_all_tiers(self):
        """Test default winter normal prices for all tiers."""
        for tier in range(4):
            price = get_import_price({}, "winter", "normal", tier)
            expected = DEFAULT_LEVERING_PRICES["winter_normal"][tier] + BELASTING_PER_TIER[tier]
            assert abs(price - expected) < 0.000001

    def test_default_summer_offpeak_weekday(self):
        """Test default summer off-peak weekday prices."""
        for tier in range(4):
            price = get_import_price({}, "summer", "offpeak_weekday", tier)
            expected = DEFAULT_LEVERING_PRICES["summer_offpeak_weekday"][tier] + BELASTING_PER_TIER[tier]
            assert abs(price - expected) < 0.000001

    def test_default_summer_offpeak_weekend(self):
        """Test default summer off-peak weekend prices (free delivery)."""
        for tier in range(4):
            price = get_import_price({}, "summer", "offpeak_weekend", tier)
            expected = DEFAULT_LEVERING_PRICES["summer_offpeak_weekend"][tier] + BELASTING_PER_TIER[tier]
            assert abs(price - expected) < 0.000001

    def test_default_winter_offpeak_day(self):
        """Test default winter off-peak day prices."""
        for tier in range(4):
            price = get_import_price({}, "winter", "offpeak_day", tier)
            expected = DEFAULT_LEVERING_PRICES["winter_offpeak_day"][tier] + BELASTING_PER_TIER[tier]
            assert abs(price - expected) < 0.000001

    def test_default_winter_offpeak_night(self):
        """Test default winter off-peak night prices."""
        for tier in range(4):
            price = get_import_price({}, "winter", "offpeak_night", tier)
            expected = DEFAULT_LEVERING_PRICES["winter_offpeak_night"][tier] + BELASTING_PER_TIER[tier]
            assert abs(price - expected) < 0.000001


class TestGetImportPriceCustomValues:
    """Test import price calculation with custom values."""

    def test_custom_levering_price_all_tiers_same(self):
        """Test custom levering prices with same value for all tiers."""
        custom_levering = 0.10
        levering_prices = {"summer_normal_levering": "0.10,0.10,0.10,0.10"}
        
        for tier in range(4):
            price = get_import_price(levering_prices, "summer", "normal", tier)
            expected = custom_levering + BELASTING_PER_TIER[tier]
            assert abs(price - expected) < 0.000001

    def test_custom_levering_price_different_tiers(self):
        """Test custom levering prices with different values per tier."""
        levering_prices = {"winter_normal_levering": "0.10,0.12,0.14,0.16"}
        expected_leveringen = [0.10, 0.12, 0.14, 0.16]
        
        for tier in range(4):
            price = get_import_price(levering_prices, "winter", "normal", tier)
            expected = expected_leveringen[tier] + BELASTING_PER_TIER[tier]
            assert abs(price - expected) < 0.000001

    def test_fallback_to_default_when_custom_not_provided(self):
        """Test that defaults are used when custom levering prices not in config."""
        levering_prices = {"winter_normal_levering": "0.10,0.12,0.14,0.16"}
        
        # For summer_normal, which is not in levering_prices, should use defaults
        for tier in range(4):
            price = get_import_price(levering_prices, "summer", "normal", tier)
            expected = DEFAULT_LEVERING_PRICES["summer_normal"][tier] + BELASTING_PER_TIER[tier]
            assert abs(price - expected) < 0.000001

    def test_zero_levering_price(self):
        """Test with zero levering price (free delivery period)."""
        levering_prices = {"summer_offpeak_weekend_levering": "0.00,0.00,0.00,0.00"}
        
        for tier in range(4):
            price = get_import_price(levering_prices, "summer", "offpeak_weekend", tier)
            expected = BELASTING_PER_TIER[tier]  # Only belasting
            assert abs(price - expected) < 0.000001

    def test_negative_levering_price(self):
        """Test with negative levering price (subsidy scenario)."""
        levering_prices = {"summer_normal_levering": "-0.05,-0.05,-0.05,-0.05"}
        
        for tier in range(4):
            price = get_import_price(levering_prices, "summer", "normal", tier)
            expected = -0.05 + BELASTING_PER_TIER[tier]
            assert abs(price - expected) < 0.000001


class TestPriceRealism:
    """Test that calculated prices are realistic."""

    def test_winter_prices_higher_than_summer(self):
        """Test that winter normal prices are typically higher than summer."""
        winter_price = get_import_price({}, "winter", "normal", 0)
        summer_price = get_import_price({}, "summer", "normal", 0)
        assert winter_price > summer_price

    def test_offpeak_prices_lower_than_normal(self):
        """Test that off-peak prices are lower than normal period prices."""
        normal_price = get_import_price({}, "summer", "normal", 0)
        offpeak_price = get_import_price({}, "summer", "offpeak_weekday", 0)
        assert offpeak_price < normal_price

    def test_belasting_is_always_positive(self):
        """Test that belasting (energy tax) is always positive."""
        for tier in range(4):
            assert BELASTING_PER_TIER[tier] > 0

    def test_prices_positive_with_defaults(self):
        """Test that all default prices are positive."""
        for season in ["summer", "winter"]:
            for period in ["normal", "offpeak_weekday", "offpeak_weekend", "offpeak_day", "offpeak_night"]:
                for tier in range(4):
                    price = get_import_price({}, season, period, tier)
                    # Price should be positive (belasting alone is positive)
                    assert price >= 0


class TestBelastungPerTier:
    """Test energy tax (belasting) per tier values."""

    def test_belasting_decreases_with_higher_consumption(self):
        """Test that belasting decreases for higher consumption tiers."""
        assert BELASTING_PER_TIER[0] == BELASTING_PER_TIER[1]  # Tiers 0 and 1 same
        assert BELASTING_PER_TIER[1] > BELASTING_PER_TIER[2]   # Tier 1 > Tier 2
        assert BELASTING_PER_TIER[2] > BELASTING_PER_TIER[3]   # Tier 2 > Tier 3

    def test_belasting_values_reasonable(self):
        """Test that belasting values are within reasonable range."""
        for tax in BELASTING_PER_TIER:
            assert 0 < tax < 0.15  # Between 0 and 0.15 €/kWh
