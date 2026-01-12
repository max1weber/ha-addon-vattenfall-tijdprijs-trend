# SPDX-License-Identifier: AGPL-3.0-only

import voluptuous as vol
from homeassistant import config_entries
from .const import *

class VattenfallConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="Vattenfall Tijdprijs",
                data=user_input,
            )

        schema = vol.Schema({
            vol.Required(CONF_IMPORT_PRICE): vol.Coerce(float),
            vol.Required(CONF_EXPORT_PRICE): vol.Coerce(float),
            vol.Required(CONF_EXPORT_COSTS): vol.Coerce(float),

            vol.Required(CONF_FIXED_DELIVERY): vol.Coerce(float),
            vol.Required(CONF_FIXED_GRID): vol.Coerce(float),
            vol.Required(CONF_FIXED_EXPORT): vol.Coerce(float),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
        )
