# SPDX-License-Identifier: AGPL-3.0-only

"""Tests for pricing data calculations."""

import pytest
from datetime import datetime
from custom_components.vattenfall_tijdprijs.pricing_data import (
    get_import_price,
    get_season,
    get_period,
    get_hourly_prices,
    BELASTING,
    DEFAULT_LEVERING_PRICES,
)


class TestGetSeason:
    """Test season determination."""
    
    def test_summer_months(self):
        """Test summer months (April-September)."""
        assert get_season(datetime(2024, 4, 15)) == "summer"
        assert get_season(datetime(2024, 6, 1)) == "summer"
        assert get_season(datetime(2024, 9, 30)) == "summer"
    
    def test_winter_months(self):
        """Test winter months (October-March)."""
        assert get_season(datetime(2024, 1, 15)) == "winter"
        assert get_season(datetime(2024, 3, 31)) == "winter"
        assert get_season(datetime(2024, 10, 1)) == "winter"
        assert get_season(datetime(2024, 12, 25)) == "winter"


class TestGetPeriod:
    """Test time-of-use period determination."""
    
    def test_summer_normal_morning(self):
        """Test summer normal period (00:00-12:00)."""
        dt = datetime(2024, 6, 10, 8, 0)  # Monday 08:00
        assert get_period(dt, "summer") in ["normal", "offpeakweekday", "offpeakweekend"]
    
    def test_summer_normal_evening(self):
        """Test summer normal period (18:00-24:00)."""
        dt = datetime(2024, 6, 10, 20, 0)  # Monday 20:00
        period = get_period(dt, "summer")
        assert period == "normal"
    
    def test_summer_offpeak_weekday(self):
        """Test summer off-peak weekday (12:00-18:00)."""
        dt = datetime(2024, 6, 10, 14, 0)  # Monday 14:00
        period = get_period(dt, "summer")
        assert "offpeak" in period
    
    def test_winter_normal(self):
        """Test winter normal period."""
        dt = datetime(2024, 1, 10, 8, 0)  # Wednesday 08:00
        period = get_period(dt, "winter")
        assert period == "normal"
    
    def test_winter_offpeak_night(self):
        """Test winter off-peak night (01:00-06:00)."""
        dt = datetime(2024, 1, 10, 3, 0)  # Wednesday 03:00
        period = get_period(dt, "winter")
        assert "offpeak" in period or period == "offpeaknight"


class TestGetHourlyPrices:
    """Test hourly price calculation."""
    
    def test_returns_24_hours_by_default(self):
        """Test that 24 hours of data is returned by default."""
        start = datetime(2024, 6, 1, 0, 0)
        prices = get_hourly_prices({}, start)
        assert len(prices) == 24
    
    def test_custom_hour_count(self):
        """Test custom number of hours."""
        start = datetime(2024, 6, 1, 0, 0)
        prices = get_hourly_prices({}, start, hours=48)
        assert len(prices) == 48
    
    def test_hourly_data_structure(self):
        """Test structure of hourly data."""
        start = datetime(2024, 6, 1, 0, 0)
        prices = get_hourly_prices({}, start, hours=1)
        
        assert len(prices) == 1
        hour_data = prices[0]
        assert "time" in hour_data
        assert "hour" in hour_data
        assert "price" in hour_data
        assert "period" in hour_data
        assert "season" in hour_data
    
    def test_prices_are_positive(self):
        """Test that all prices are positive with defaults."""
        start = datetime(2024, 6, 1, 0, 0)
        prices = get_hourly_prices({}, start)
        
        for hour_data in prices:
            assert hour_data["price"] > 0


class TestGetImportPrice:
    """Test import price calculation with default values."""

    def test_default_summer_normal(self):
        """Test default summer normal price."""
        price = get_import_price({}, "summer", "normal")
        expected = DEFAULT_LEVERING_PRICES["summer_normal"] + BELASTING
        assert abs(price - expected) < 0.000001

    def test_default_winter_normal(self):
        """Test default winter normal price."""
        price = get_import_price({}, "winter", "normal")
        expected = DEFAULT_LEVERING_PRICES["winter_normal"] + BELASTING
        assert abs(price - expected) < 0.000001

    def test_default_summer_offpeak_weekday(self):
        """Test default summer off-peak weekday price."""
        price = get_import_price({}, "summer", "offpeak_weekday")
        expected = DEFAULT_LEVERING_PRICES["summer_offpeak_weekday"] + BELASTING
        assert abs(price - expected) < 0.000001

    def test_default_summer_offpeak_weekend(self):
        """Test default summer off-peak weekend price (free delivery)."""
        price = get_import_price({}, "summer", "offpeak_weekend")
        expected = DEFAULT_LEVERING_PRICES["summer_offpeak_weekend"] + BELASTING
        assert abs(price - expected) < 0.000001

    def test_default_winter_offpeak_day(self):
        """Test default winter off-peak day price."""
        price = get_import_price({}, "winter", "offpeak_day")
        expected = DEFAULT_LEVERING_PRICES["winter_offpeak_day"] + BELASTING
        assert abs(price - expected) < 0.000001

    def test_default_winter_offpeak_night(self):
        """Test default winter off-peak night price."""
        price = get_import_price({}, "winter", "offpeak_night")
        expected = DEFAULT_LEVERING_PRICES["winter_offpeak_night"] + BELASTING
        assert abs(price - expected) < 0.000001


class TestGetImportPriceCustomValues:
    """Test import price calculation with custom values."""

    def test_custom_levering_price(self):
        """Test custom levering price."""
        custom_levering = 0.10
        levering_prices = {"summer_normal_levering": custom_levering}
        
        price = get_import_price(levering_prices, "summer", "normal")
        expected = custom_levering + BELASTING
        assert abs(price - expected) < 0.000001

    def test_fallback_to_default_when_custom_not_provided(self):
        """Test that defaults are used when custom levering prices not in config."""
        levering_prices = {"winter_normal_levering": 0.10}
        
        # For summer_normal, which is not in levering_prices, should use defaults
        price = get_import_price(levering_prices, "summer", "normal")
        expected = DEFAULT_LEVERING_PRICES["summer_normal"] + BELASTING
        assert abs(price - expected) < 0.000001

    def test_zero_levering_price(self):
        """Test with zero levering price (free delivery period)."""
        levering_prices = {"summer_offpeak_weekend_levering": 0.00}
        
        price = get_import_price(levering_prices, "summer", "offpeak_weekend")
        expected = BELASTING  # Only belasting
        assert abs(price - expected) < 0.000001

    def test_negative_levering_price(self):
        """Test with negative levering price (subsidy scenario)."""
        levering_prices = {"summer_normal_levering": -0.05}
        
        price = get_import_price(levering_prices, "summer", "normal")
        expected = -0.05 + BELASTING
        assert abs(price - expected) < 0.000001


class TestPriceRealism:
    """Test that calculated prices are realistic."""

    def test_winter_prices_higher_than_summer(self):
        """Test that winter normal prices are typically higher than summer."""
        winter_price = get_import_price({}, "winter", "normal")
        summer_price = get_import_price({}, "summer", "normal")
        assert winter_price > summer_price

    def test_offpeak_prices_lower_than_normal(self):
        """Test that off-peak prices are lower than normal period prices."""
        normal_price = get_import_price({}, "summer", "normal")
        offpeak_price = get_import_price({}, "summer", "offpeak_weekday")
        assert offpeak_price < normal_price

    def test_belasting_is_positive(self):
        """Test that belasting (energy tax) is positive."""
        assert BELASTING > 0

    def test_prices_positive_with_defaults(self):
        """Test that all default prices are positive."""
        for season in ["summer", "winter"]:
            for period in ["normal", "offpeak_weekday", "offpeak_weekend", "offpeak_day", "offpeak_night"]:
                try:
                    price = get_import_price({}, season, period)
                    # Price should be positive or zero (belasting is always positive)
                    assert price >= 0
                except KeyError:
                    # Some combinations don't exist (like summer offpeak_day)
                    pass


class TestBelasting:
    """Test energy tax (belasting) value."""

    def test_belasting_value_reasonable(self):
        """Test that belasting value is within reasonable range."""
        assert 0 < BELASTING < 0.15  # Between 0 and 0.15 €/kWh
