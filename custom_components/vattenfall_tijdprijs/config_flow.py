# SPDX-License-Identifier: AGPL-3.0-only

import voluptuous as vol
from homeassistant import config_entries
from .const import (
    CONF_EXPORT_COSTS,
    CONF_EXPORT_PRICE,
    CONF_FIXED_DELIVERY,
    CONF_FIXED_EXPORT,
    CONF_FIXED_GRID,
    CONF_IMPORT_PRICE,
    DEFAULT_EXPORT_COSTS,
    DEFAULT_EXPORT_PRICE,
    DEFAULT_FIXED_DELIVERY,
    DEFAULT_FIXED_EXPORT,
    DEFAULT_FIXED_GRID,
    DEFAULT_IMPORT_PRICE,
    DOMAIN,
)

class VattenfallConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="Vattenfall Tijdprijs",
                data=user_input,
            )

        price_validator = vol.All(vol.Coerce(float), vol.Range(min=0, max=1000))

        schema = vol.Schema({
            vol.Required(CONF_IMPORT_PRICE, default=DEFAULT_IMPORT_PRICE): price_validator,
            vol.Required(CONF_EXPORT_PRICE, default=DEFAULT_EXPORT_PRICE): price_validator,
            vol.Required(CONF_EXPORT_COSTS, default=DEFAULT_EXPORT_COSTS): price_validator,
            vol.Required(CONF_FIXED_DELIVERY, default=DEFAULT_FIXED_DELIVERY): price_validator,
            vol.Required(CONF_FIXED_GRID, default=DEFAULT_FIXED_GRID): price_validator,
            vol.Required(CONF_FIXED_EXPORT, default=DEFAULT_FIXED_EXPORT): price_validator,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
        )
