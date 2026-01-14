# SPDX-License-Identifier: AGPL-3.0-only

"""Constants for the Vattenfall Tijdprijs integration."""

# Default values
DEFAULT_NAME = "Vattenfall Tijdprijs"

# Default price values (€)
DEFAULT_IMPORT_PRICE = 0.30
DEFAULT_EXPORT_PRICE = 0.10
DEFAULT_EXPORT_COSTS = 0.03
DEFAULT_FIXED_DELIVERY = 0.50
DEFAULT_FIXED_GRID = 0.60
DEFAULT_FIXED_EXPORT = 0.15

DOMAIN = "vattenfall_tijdprijs"
NAME = "Vattenfall Tijdprijs"
VERSION = "1.0.0"

CONF_IMPORT_PRICE = "import_price"
CONF_EXPORT_PRICE = "export_price"
CONF_EXPORT_COSTS = "export_costs"

CONF_FIXED_DELIVERY = "fixed_delivery_costs"
CONF_FIXED_GRID = "fixed_grid_costs"
CONF_FIXED_EXPORT = "fixed_export_costs"

DEFAULT_CURRENCY = "EUR"
DEFAULT_UNIT_PRICE = "€/kWh"
DEFAULT_UNIT_FIXED = "€/dag"
