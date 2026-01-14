# SPDX-License-Identifier: AGPL-3.0-only

"""Pricing data for Vattenfall TijdPrijs with time-of-use and usage tiers."""

# Fixed energy tax rates per tier (kWh/year: 0, 2900, 10000, 50000)
# These are government-set and the same for all periods
# All prices in €/kWh including VAT
BELASTING_PER_TIER = [0.110848, 0.110848, 0.080719, 0.045194]

# Default delivery (levering) prices per time period and tier
# These are Vattenfall-specific and can vary
DEFAULT_LEVERING_PRICES = {
    "summer_normal": [0.115434, 0.115434, 0.115434, 0.115434],
    "summer_offpeak_weekday": [0.017908, 0.017908, 0.017908, 0.017908],
    "summer_offpeak_weekend": [0.000000, 0.000000, 0.000000, 0.000000],
    "winter_normal": [0.140723, 0.140723, 0.140723, 0.140723],
    "winter_offpeak_day": [0.087483, 0.087483, 0.087483, 0.087483],
    "winter_offpeak_night": [0.070785, 0.070785, 0.070785, 0.070785],
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


def get_tier_index(annual_consumption_kwh: float) -> int:
    """Determine the pricing tier based on annual consumption."""
    if annual_consumption_kwh >= 50000:
        return 3
    elif annual_consumption_kwh >= 10000:
        return 2
    elif annual_consumption_kwh >= 2900:
        return 1
    else:
        return 0


def get_import_price(levering_prices: dict, season: str, period: str, tier_index: int) -> float:
    """Get the import price for a given season, period, and tier.
    
    Args:
        levering_prices: Dict with levering prices per period (from config)
        season: 'summer' or 'winter'
        period: Time period name
        tier_index: Usage tier (0-3)
    
    Returns:
        Total price (levering + belasting) in €/kWh
    """
    period_key = f"{season}_{period}"
    config_key = f"{period_key}_levering"
    
    # Get levering price from config or use default
    if config_key in levering_prices:
        # Stored as comma-separated string of 4 tier prices
        tier_prices = [float(x) for x in levering_prices[config_key].split(",")]
        levering = tier_prices[tier_index]
    else:
        levering = DEFAULT_LEVERING_PRICES.get(period_key, [0]*4)[tier_index]
    
    # Belasting is fixed per tier
    belasting = BELASTING_PER_TIER[tier_index]
    
    return levering + belasting

