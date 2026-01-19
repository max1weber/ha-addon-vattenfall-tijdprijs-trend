# SPDX-License-Identifier: AGPL-3.0-only

"""Constants for the Vattenfall Tijdprijs integration."""

DOMAIN = "vattenfall_tijdprijs"
NAME = "Vattenfall Tijdprijs"
VERSION = "1.1.0"

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

# Unit constants
DEFAULT_UNIT_PRICE = "€/kWh"
DEFAULT_UNIT_FIXED = "€/dag"
