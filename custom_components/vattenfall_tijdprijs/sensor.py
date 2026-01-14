# SPDX-License-Identifier: AGPL-3.0-only

from homeassistant.components.sensor import SensorEntity
from .const import (
    CONF_EXPORT_COSTS,
    CONF_EXPORT_COMPENSATION,
    CONF_FIXED_DELIVERY,
    CONF_FIXED_GRID,
    CONF_FIXED_TAX_REDUCTION,
    DEFAULT_UNIT_PRICE,
    DEFAULT_UNIT_FIXED,
)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Vattenfall Tijdprijs sensors."""
    data = entry.data

    sensors = [
        PriceSensor("Terugleververgoeding", data[CONF_EXPORT_COMPENSATION], DEFAULT_UNIT_PRICE),
        PriceSensor("Terugleverkosten", data[CONF_EXPORT_COSTS], DEFAULT_UNIT_PRICE),

        FixedCostSensor("Vaste leveringskosten", data[CONF_FIXED_DELIVERY]),
        FixedCostSensor("Vaste belastingvermindering", data[CONF_FIXED_TAX_REDUCTION]),
        FixedCostSensor("Vaste netbeheerkosten", data[CONF_FIXED_GRID]),
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
