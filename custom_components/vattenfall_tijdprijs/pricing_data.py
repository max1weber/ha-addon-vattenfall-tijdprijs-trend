# SPDX-License-Identifier: AGPL-3.0-only

"""Pricing data for Vattenfall TijdPrijs with time-of-use periods."""

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

