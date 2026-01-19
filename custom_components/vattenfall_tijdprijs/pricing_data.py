# SPDX-License-Identifier: AGPL-3.0-only

"""Pricing data for Vattenfall TijdPrijs with time-of-use periods."""

from datetime import datetime, timedelta

# Fixed energy tax rate (government-set, same for all periods)
# All prices in €/kWh including VAT
# Using the standard rate for typical household consumption (0-10000 kWh/year)
BELASTING = 0.110848

# Default delivery (levering) prices per time period
# These are Vattenfall-specific and can vary
DEFAULT_LEVERING_PRICES = {
    "summer_normal": 0.115434,
    "summer_offpeak_weekday": 0.017908,
    "summer_offpeak_weekend": 0.000000,
    "winter_normal": 0.140723,
    "winter_offpeak_day": 0.087483,
    "winter_offpeak_night": 0.070785,
}

# Configuration keys for storing levering prices
LEVERING_CONFIG_KEYS = [
    "summer_normal_levering",
    "summer_offpeak_weekday_levering",
    "summer_offpeak_weekend_levering",
    "winter_normal_levering",
    "winter_offpeak_day_levering",
    "winter_offpeak_night_levering",
]

# Period labels for UI
PERIOD_LABELS = {
    "summer_normal": "Zomer normaal (00:00-12:00, 18:00-24:00)",
    "summer_offpeak_weekday": "Zomer dal week (12:00-16:00)",
    "summer_offpeak_weekend": "Zomer dal weekend (12:00-16:00)",
    "winter_normal": "Winter normaal (06:00-12:00, 16:00-01:00)",
    "winter_offpeak_day": "Winter dal dag (12:00-16:00)",
    "winter_offpeak_night": "Winter dal nacht (01:00-06:00)",
}

# Season definitions
SUMMER_MONTHS = range(4, 10)  # April to September
WINTER_MONTHS = list(range(1, 4)) + list(range(10, 13))  # Oct-Mar

# Time-of-use periods (hour ranges)
TOU_PERIODS = {
    "summer": {
        "normal": [(0, 12), (18, 24)],
        "offpeak_weekday": [(12, 18)],
        "offpeak_weekend": [(12, 18)],
    },
    "winter": {
        "normal": [(6, 12), (16, 24), (0, 1)],
        "offpeak_day": [(12, 16)],
        "offpeak_night": [(1, 6)],
    },
}


def get_season(dt: datetime) -> str:
    """Determine season (summer or winter) for a given datetime."""
    return "summer" if dt.month in SUMMER_MONTHS else "winter"


def get_period(dt: datetime, season: str) -> str:
    """Determine time-of-use period for a given datetime and season."""
    hour = dt.hour
    is_weekend = dt.weekday() >= 5  # Saturday=5, Sunday=6
    
    periods = TOU_PERIODS[season]
    
    # Check each period to see if hour falls within it
    for period_name, time_ranges in periods.items():
        for start_hour, end_hour in time_ranges:
            if start_hour <= hour < end_hour:
                # Handle weekend vs weekday for summer off-peak
                if season == "summer" and "offpeak" in period_name:
                    return "offpeak_weekend" if is_weekend else "offpeak_weekday"
                return period_name.replace("_", "")  # Remove underscore for consistency
    
    # Default fallback (shouldn't happen if TOU_PERIODS is complete)
    return "normal"


def get_import_price(levering_prices: dict, season: str, period: str) -> float:
    """Get the import price for a given season and period.
    
    Args:
        levering_prices: Dict with levering prices per period (from config)
        season: 'summer' or 'winter'
        period: Time period name
    
    Returns:
        Total price (levering + belasting) in €/kWh
    """
    period_key = f"{season}_{period}"
    config_key = f"{period_key}_levering"
    
    # Get levering price from config or use default
    if config_key in levering_prices:
        levering = float(levering_prices[config_key])
    else:
        levering = DEFAULT_LEVERING_PRICES.get(period_key, 0)
    
    # Belasting is fixed
    return levering + BELASTING


def get_hourly_prices(levering_prices: dict, start_time: datetime, hours: int = 24) -> list:
    """Get hourly prices for the next N hours.
    
    Args:
        levering_prices: Dict with levering prices per period (from config)
        start_time: Starting datetime
        hours: Number of hours to calculate (default 24)
    
    Returns:
        List of dicts with 'time' and 'price' for each hour
    """
    hourly_data = []
    
    for i in range(hours):
        dt = start_time + timedelta(hours=i)
        season = get_season(dt)
        period = get_period(dt, season)
        price = get_import_price(levering_prices, season, period)
        
        hourly_data.append({
            "time": dt.isoformat(),
            "hour": dt.hour,
            "price": round(price, 6),
            "period": period,
            "season": season,
        })
    
    return hourly_data

