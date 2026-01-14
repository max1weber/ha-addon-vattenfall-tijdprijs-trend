# SPDX-License-Identifier: AGPL-3.0-only

"""Pricing data for Vattenfall TijdPrijs with time-of-use and usage tiers."""

# Pricing structure based on usage tiers (kWh/year: 0, 2900, 10000, 50000)
# All prices in €/kWh including VAT

SUMMER_NORMAL_PRICING = {
    "levering": [0.115434, 0.115434, 0.115434, 0.115434],
    "belasting": [0.110848, 0.110848, 0.080719, 0.045194],
}

SUMMER_OFFPEAK_WEEKDAY_PRICING = {
    "levering": [0.017908, 0.017908, 0.017908, 0.017908],
    "belasting": [0.110848, 0.110848, 0.080719, 0.045194],
}

SUMMER_OFFPEAK_WEEKEND_PRICING = {
    "levering": [0.000000, 0.000000, 0.000000, 0.000000],
    "belasting": [0.110848, 0.110848, 0.080719, 0.045194],
}

WINTER_NORMAL_PRICING = {
    "levering": [0.140723, 0.140723, 0.140723, 0.140723],
    "belasting": [0.110848, 0.110848, 0.080719, 0.045194],
}

WINTER_OFFPEAK_DAY_PRICING = {
    "levering": [0.087483, 0.087483, 0.087483, 0.087483],
    "belasting": [0.110848, 0.110848, 0.080719, 0.045194],
}

WINTER_OFFPEAK_NIGHT_PRICING = {
    "levering": [0.070785, 0.070785, 0.070785, 0.070785],
    "belasting": [0.110848, 0.110848, 0.080719, 0.045194],
}

# Fixed costs per day (€/day)
FIXED_COSTS = {
    "levering": 0.295572,
    "belasting_reduction": -1.723173,  # Tax reduction (negative = credit)
    "grid": 1.303654,
}

# Export pricing (yearly tariff)
EXPORT_PRICING = {
    "compensation": -0.134000,  # BTW-vrij tarief (negative = you receive money)
    "costs": 0.055781,
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


def get_import_price(season: str, period: str, tier_index: int) -> float:
    """Get the import price for a given season, period, and tier."""
    pricing_map = {
        "summer": {
            "normal": SUMMER_NORMAL_PRICING,
            "off_peak_weekday": SUMMER_OFFPEAK_WEEKDAY_PRICING,
            "off_peak_weekend": SUMMER_OFFPEAK_WEEKEND_PRICING,
        },
        "winter": {
            "normal": WINTER_NORMAL_PRICING,
            "off_peak_day": WINTER_OFFPEAK_DAY_PRICING,
            "off_peak_night": WINTER_OFFPEAK_NIGHT_PRICING,
        },
    }
    
    pricing = pricing_map.get(season, {}).get(period, SUMMER_NORMAL_PRICING)
    levering = pricing["levering"][tier_index]
    belasting = pricing["belasting"][tier_index]
    
    return levering + belasting
