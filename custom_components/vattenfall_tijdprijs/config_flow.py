# SPDX-License-Identifier: AGPL-3.0-only

"""Config flow for Vattenfall Tijdprijs integration."""

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import (
    CONF_EXPORT_COMPENSATION,
    CONF_EXPORT_COSTS,
    CONF_FIXED_DELIVERY,
    CONF_FIXED_GRID,
    CONF_FIXED_TAX_REDUCTION,
    DEFAULT_EXPORT_COMPENSATION,
    DEFAULT_EXPORT_COSTS,
    DEFAULT_FIXED_DELIVERY,
    DEFAULT_FIXED_GRID,
    DEFAULT_FIXED_TAX_REDUCTION,
    DOMAIN,
)


class VattenfallConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Vattenfall Tijdprijs."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step - creates entry with all defaults."""
        if user_input is not None:
            # Create entry with provided data merged with defaults
            data = {
                CONF_FIXED_DELIVERY: user_input.get(
                    CONF_FIXED_DELIVERY, DEFAULT_FIXED_DELIVERY
                ),
                CONF_FIXED_TAX_REDUCTION: user_input.get(
                    CONF_FIXED_TAX_REDUCTION, DEFAULT_FIXED_TAX_REDUCTION
                ),
                CONF_FIXED_GRID: user_input.get(CONF_FIXED_GRID, DEFAULT_FIXED_GRID),
                CONF_EXPORT_COMPENSATION: user_input.get(
                    CONF_EXPORT_COMPENSATION, DEFAULT_EXPORT_COMPENSATION
                ),
                CONF_EXPORT_COSTS: user_input.get(
                    CONF_EXPORT_COSTS, DEFAULT_EXPORT_COSTS
                ),
            }

            return self.async_create_entry(
                title="Vattenfall Tijdprijs",
                data=data,
            )

        # Show simple form - all fields optional, will use defaults if not provided
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
        )
