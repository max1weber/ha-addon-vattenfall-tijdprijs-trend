# SPDX-License-Identifier: AGPL-3.0-only

"""Constants for the Vattenfall Tijdprijs integration."""

DOMAIN = "vattenfall_tijdprijs"
NAME = "Vattenfall Tijdprijs"
VERSION = "1.1.0"

# Configuration keys
CONF_ANNUAL_CONSUMPTION = "annual_consumption"
CONF_USE_CONSUMPTION_SENSOR = "use_consumption_sensor"
CONF_CONSUMPTION_SENSOR = "consumption_sensor"

# Fixed costs configuration
CONF_FIXED_DELIVERY = "fixed_delivery_costs"
CONF_FIXED_TAX_REDUCTION = "fixed_tax_reduction"
CONF_FIXED_GRID = "fixed_grid_costs"
CONF_EXPORT_COMPENSATION = "export_compensation"
CONF_EXPORT_COSTS = "export_costs"

# Default values for fixed costs (per day)
DEFAULT_FIXED_DELIVERY = 0.295572
DEFAULT_FIXED_TAX_REDUCTION = -1.723173
DEFAULT_FIXED_GRID = 1.303654

# Default values for export (yearly rates)
DEFAULT_EXPORT_COMPENSATION = -0.134000
DEFAULT_EXPORT_COSTS = 0.055781

# Default annual consumption for tier calculation
DEFAULT_ANNUAL_CONSUMPTION = 3000

# Usage tiers (kWh per year)
USAGE_TIERS = [0, 2900, 10000, 50000]

# Time-of-use periods configuration
# Format: (start_hour, end_hour) - hours in 24h format
TOU_PERIODS = {
    "summer": {
        "normal": [
            (0, 12),    # 00:00-12:00
            (18, 24),   # 18:00-24:00
        ],
        "off_peak_weekday": [(12, 16)],     # 12:00-16:00
        "off_peak_weekend": [(12, 16)],     # 12:00-16:00
    },
    "winter": {
        "normal": [
            (6, 12),    # 06:00-12:00
            (16, 24),   # 16:00-01:00 (continues to next day)
            (0, 1),     # 00:00-01:00
        ],
        "off_peak_day": [(12, 16)],         # 12:00-16:00
        "off_peak_night": [(1, 6)],         # 01:00-06:00
    },
}

# Season definitions (month ranges)
SUMMER_MONTHS = range(4, 10)  # April to September (months 4-9)
WINTER_MONTHS = list(range(1, 4)) + list(range(10, 13))  # Oct-Mar (months 1-3, 10-12)
