# SPDX-License-Identifier: AGPL-3.0-only

"""Constants for the Vattenfall Tijdprijs integration."""

# Default values
DEFAULT_NAME = "Vattenfall Tijdprijs"



DOMAIN = "vattenfall_tijdprijs"
NAME = "Vattenfall Tijdprijs"
VERSION = "1.0.0"

# API Configuration
API_TIMEOUT = 30
UPDATE_INTERVAL = 900  # 15 minutes in seconds
CONF_IMPORT_PRICE = "import_price"
CONF_EXPORT_PRICE = "export_price"
CONF_EXPORT_COSTS = "export_costs"

CONF_FIXED_DELIVERY = "fixed_delivery_costs"
CONF_FIXED_GRID = "fixed_grid_costs"
CONF_FIXED_EXPORT = "fixed_export_costs"

DEFAULT_CURRENCY = "EUR"
DEFAULT_UNIT_PRICE = "€/kWh"
DEFAULT_UNIT_FIXED = "€/dag"
