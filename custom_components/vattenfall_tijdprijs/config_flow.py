# SPDX-License-Identifier: AGPL-3.0-only

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.selector import (
    NumberSelector,
    NumberSelectorConfig,
)

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
from .pricing_data import DEFAULT_LEVERING_PRICES, PERIOD_LABELS


class VattenfallConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Vattenfall Tijdprijs."""

    VERSION = 1

    def __init__(self):
        """Initialize the config flow."""
        self._data = {}

    async def async_step_user(self, user_input=None):
        """Handle the initial step - fixed costs configuration."""
        if user_input is not None:
            self._data.update(user_input)
            # Ask if user wants to configure custom pricing
            return await self.async_step_pricing_choice()

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
            step_id="user",
            data_schema=schema,
        )

    async def async_step_pricing_choice(self, user_input=None):
        """Ask if user wants to configure custom pricing."""
        if user_input is not None:
            if user_input.get("configure_pricing", False):
                return await self.async_step_pricing_summer_normal()
            else:
                return await self.async_step_export()

        schema = vol.Schema(
            {
                vol.Required("configure_pricing", default=False): cv.boolean,
            }
        )

        return self.async_show_form(
            step_id="pricing_choice",
            data_schema=schema,
        )

    async def async_step_pricing_summer_normal(self, user_input=None):
        """Configure summer normal period pricing."""
        if user_input is not None:
            self._data.update(user_input)
            return await self.async_step_pricing_summer_offpeak_weekday()

        default_price = DEFAULT_LEVERING_PRICES["summer_normal"]
        schema = vol.Schema(
            {
                vol.Required("summer_normal_levering", default=default_price): NumberSelector(
                    NumberSelectorConfig(min=-1, max=1, step=0.000001, unit_of_measurement="€/kWh", mode="box")
                ),
            }
        )

        return self.async_show_form(
            step_id="pricing_summer_normal",
            data_schema=schema,
            description_placeholders={"period": PERIOD_LABELS["summer_normal"]},
        )

    async def async_step_pricing_summer_offpeak_weekday(self, user_input=None):
        """Configure summer off-peak weekday pricing."""
        if user_input is not None:
            self._data.update(user_input)
            return await self.async_step_pricing_summer_offpeak_weekend()

        default_price = DEFAULT_LEVERING_PRICES["summer_offpeak_weekday"]
        schema = vol.Schema(
            {
                vol.Required("summer_offpeak_weekday_levering", default=default_price): NumberSelector(
                    NumberSelectorConfig(min=-1, max=1, step=0.000001, unit_of_measurement="€/kWh", mode="box")
                ),
            }
        )

        return self.async_show_form(
            step_id="pricing_summer_offpeak_weekday",
            data_schema=schema,
            description_placeholders={"period": PERIOD_LABELS["summer_offpeak_weekday"]},
        )

    async def async_step_pricing_summer_offpeak_weekend(self, user_input=None):
        """Configure summer off-peak weekend pricing."""
        if user_input is not None:
            self._data.update(user_input)
            return await self.async_step_pricing_winter_normal()

        default_price = DEFAULT_LEVERING_PRICES["summer_offpeak_weekend"]
        schema = vol.Schema(
            {
                vol.Required("summer_offpeak_weekend_levering", default=default_price): NumberSelector(
                    NumberSelectorConfig(min=-1, max=1, step=0.000001, unit_of_measurement="€/kWh", mode="box")
                ),
            }
        )

        return self.async_show_form(
            step_id="pricing_summer_offpeak_weekend",
            data_schema=schema,
            description_placeholders={"period": PERIOD_LABELS["summer_offpeak_weekend"]},
        )

    async def async_step_pricing_winter_normal(self, user_input=None):
        """Configure winter normal period pricing."""
        if user_input is not None:
            self._data.update(user_input)
            return await self.async_step_pricing_winter_offpeak_day()

        default_price = DEFAULT_LEVERING_PRICES["winter_normal"]
        schema = vol.Schema(
            {
                vol.Required("winter_normal_levering", default=default_price): NumberSelector(
                    NumberSelectorConfig(min=-1, max=1, step=0.000001, unit_of_measurement="€/kWh", mode="box")
                ),
            }
        )

        return self.async_show_form(
            step_id="pricing_winter_normal",
            data_schema=schema,
            description_placeholders={"period": PERIOD_LABELS["winter_normal"]},
        )

    async def async_step_pricing_winter_offpeak_day(self, user_input=None):
        """Configure winter off-peak day pricing."""
        if user_input is not None:
            self._data.update(user_input)
            return await self.async_step_pricing_winter_offpeak_night()

        default_price = DEFAULT_LEVERING_PRICES["winter_offpeak_day"]
        schema = vol.Schema(
            {
                vol.Required("winter_offpeak_day_levering", default=default_price): NumberSelector(
                    NumberSelectorConfig(min=-1, max=1, step=0.000001, unit_of_measurement="€/kWh", mode="box")
                ),
            }
        )

        return self.async_show_form(
            step_id="pricing_winter_offpeak_day",
            data_schema=schema,
            description_placeholders={"period": PERIOD_LABELS["winter_offpeak_day"]},
        )

    async def async_step_pricing_winter_offpeak_night(self, user_input=None):
        """Configure winter off-peak night pricing."""
        if user_input is not None:
            self._data.update(user_input)
            return await self.async_step_export()

        default_price = DEFAULT_LEVERING_PRICES["winter_offpeak_night"]
        schema = vol.Schema(
            {
                vol.Required("winter_offpeak_night_levering", default=default_price): NumberSelector(
                    NumberSelectorConfig(min=-1, max=1, step=0.000001, unit_of_measurement="€/kWh", mode="box")
                ),
            }
        )

        return self.async_show_form(
            step_id="pricing_winter_offpeak_night",
            data_schema=schema,
            description_placeholders={"period": PERIOD_LABELS["winter_offpeak_night"]},
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
