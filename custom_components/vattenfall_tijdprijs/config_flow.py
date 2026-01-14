# SPDX-License-Identifier: AGPL-3.0-only

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    NumberSelector,
    NumberSelectorConfig,
)

from .const import (
    CONF_ANNUAL_CONSUMPTION,
    CONF_CONSUMPTION_SENSOR,
    CONF_EXPORT_COMPENSATION,
    CONF_EXPORT_COSTS,
    CONF_FIXED_DELIVERY,
    CONF_FIXED_GRID,
    CONF_FIXED_TAX_REDUCTION,
    CONF_USE_CONSUMPTION_SENSOR,
    DEFAULT_ANNUAL_CONSUMPTION,
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

    def __init__(self):
        """Initialize the config flow."""
        self._data = {}

    async def async_step_user(self, user_input=None):
        """Handle the initial step - consumption configuration."""
        errors = {}

        if user_input is not None:
            self._data.update(user_input)
            return await self.async_step_fixed_costs()

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_USE_CONSUMPTION_SENSOR,
                    default=False,
                ): cv.boolean,
                vol.Optional(
                    CONF_ANNUAL_CONSUMPTION,
                    default=DEFAULT_ANNUAL_CONSUMPTION,
                ): NumberSelector(
                    NumberSelectorConfig(
                        min=0,
                        max=100000,
                        step=100,
                        unit_of_measurement="kWh",
                        mode="box",
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
            description_placeholders={
                "title": "Jaarverbruik configuratie",
            },
        )

    async def async_step_consumption_sensor(self, user_input=None):
        """Handle consumption sensor configuration."""
        errors = {}

        if user_input is not None:
            self._data.update(user_input)
            return await self.async_step_fixed_costs()

        if not self._data.get(CONF_USE_CONSUMPTION_SENSOR):
            return await self.async_step_fixed_costs()

        schema = vol.Schema(
            {
                vol.Required(CONF_CONSUMPTION_SENSOR): EntitySelector(
                    EntitySelectorConfig(domain="sensor")
                ),
            }
        )

        return self.async_show_form(
            step_id="consumption_sensor",
            data_schema=schema,
            errors=errors,
        )

    async def async_step_fixed_costs(self, user_input=None):
        """Handle fixed costs configuration."""
        if user_input is not None:
            self._data.update(user_input)
            return await self.async_step_export()

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_FIXED_DELIVERY,
                    default=DEFAULT_FIXED_DELIVERY,
                ): NumberSelector(
                    NumberSelectorConfig(
                        min=-10,
                        max=10,
                        step=0.000001,
                        unit_of_measurement="€/dag",
                        mode="box",
                    )
                ),
                vol.Required(
                    CONF_FIXED_TAX_REDUCTION,
                    default=DEFAULT_FIXED_TAX_REDUCTION,
                ): NumberSelector(
                    NumberSelectorConfig(
                        min=-10,
                        max=10,
                        step=0.000001,
                        unit_of_measurement="€/dag",
                        mode="box",
                    )
                ),
                vol.Required(
                    CONF_FIXED_GRID,
                    default=DEFAULT_FIXED_GRID,
                ): NumberSelector(
                    NumberSelectorConfig(
                        min=0,
                        max=10,
                        step=0.000001,
                        unit_of_measurement="€/dag",
                        mode="box",
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="fixed_costs",
            data_schema=schema,
        )

    async def async_step_export(self, user_input=None):
        """Handle export pricing configuration."""
        if user_input is not None:
            self._data.update(user_input)
            return self.async_create_entry(
                title="Vattenfall Tijdprijs",
                data=self._data,
            )

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_EXPORT_COMPENSATION,
                    default=DEFAULT_EXPORT_COMPENSATION,
                ): NumberSelector(
                    NumberSelectorConfig(
                        min=-1,
                        max=0,
                        step=0.000001,
                        unit_of_measurement="€/kWh",
                        mode="box",
                    )
                ),
                vol.Required(
                    CONF_EXPORT_COSTS,
                    default=DEFAULT_EXPORT_COSTS,
                ): NumberSelector(
                    NumberSelectorConfig(
                        min=0,
                        max=1,
                        step=0.000001,
                        unit_of_measurement="€/kWh",
                        mode="box",
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="export",
            data_schema=schema,
        )

