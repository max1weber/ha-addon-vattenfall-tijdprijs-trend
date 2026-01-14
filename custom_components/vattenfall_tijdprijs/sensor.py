# SPDX-License-Identifier: AGPL-3.0-only

from homeassistant.components.sensor import SensorEntity
from .const import (
    CONF_IMPORT_PRICE,
    CONF_EXPORT_PRICE,
    CONF_EXPORT_COSTS,
    CONF_FIXED_DELIVERY,
    CONF_FIXED_GRID,
    CONF_FIXED_EXPORT,
    DEFAULT_UNIT_PRICE,
    DEFAULT_UNIT_FIXED,
)

async def async_setup_entry(hass, entry, async_add_entities):
    data = entry.data

    sensors = [
        PriceSensor("Import prijs", data[CONF_IMPORT_PRICE], DEFAULT_UNIT_PRICE),
        PriceSensor("Terugleververgoeding", data[CONF_EXPORT_PRICE], DEFAULT_UNIT_PRICE),
        PriceSensor("Terugleverkosten", data[CONF_EXPORT_COSTS], DEFAULT_UNIT_PRICE),

        FixedCostSensor("Vaste leveringskosten", data[CONF_FIXED_DELIVERY]),
        FixedCostSensor("Vaste netbeheerkosten", data[CONF_FIXED_GRID]),
        FixedCostSensor("Vaste terugleverkosten", data[CONF_FIXED_EXPORT]),
    ]

    async_add_entities(sensors)


class PriceSensor(SensorEntity):
    def __init__(self, name, value, unit):
        self._attr_name = name
        self._attr_native_value = value
        self._attr_native_unit_of_measurement = unit


class FixedCostSensor(SensorEntity):
    def __init__(self, name, value):
        self._attr_name = name
        self._attr_native_value = value
        self._attr_native_unit_of_measurement = DEFAULT_UNIT_FIXED
