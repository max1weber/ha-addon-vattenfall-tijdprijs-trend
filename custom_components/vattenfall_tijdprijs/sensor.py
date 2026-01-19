# SPDX-License-Identifier: AGPL-3.0-only

from datetime import datetime
from homeassistant.components.sensor import SensorEntity, SensorStateClass
from .const import (
    CONF_EXPORT_COSTS,
    CONF_EXPORT_COMPENSATION,
    CONF_FIXED_DELIVERY,
    CONF_FIXED_GRID,
    CONF_FIXED_TAX_REDUCTION,
    DEFAULT_UNIT_PRICE,
    DEFAULT_UNIT_FIXED,
)
from .pricing_data import get_hourly_prices, get_season, get_period, get_import_price

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Vattenfall Tijdprijs sensors."""
    data = entry.data

    sensors = [
        # Current price sensor
        CurrentPriceSensor(data, "Huidige Importprijs"),
        
        # Hourly forecast sensor
        HourlyPriceSensor(data, "Importprijs per uur"),
        
        # Export sensors
        PriceSensor("Terugleververgoeding", data[CONF_EXPORT_COMPENSATION], DEFAULT_UNIT_PRICE),
        PriceSensor("Terugleverkosten", data[CONF_EXPORT_COSTS], DEFAULT_UNIT_PRICE),

        # Fixed cost sensors
        FixedCostSensor("Vaste leveringskosten", data[CONF_FIXED_DELIVERY]),
        FixedCostSensor("Vaste belastingvermindering", data[CONF_FIXED_TAX_REDUCTION]),
        FixedCostSensor("Vaste netbeheerkosten", data[CONF_FIXED_GRID]),
    ]

    async_add_entities(sensors)


class CurrentPriceSensor(SensorEntity):
    """Sensor for current import price based on time-of-use."""
    
    def __init__(self, config_data, name):
        """Initialize the sensor."""
        self._config_data = config_data
        self._attr_name = name
        self._attr_native_unit_of_measurement = DEFAULT_UNIT_PRICE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:currency-eur"
        
    @property
    def native_value(self):
        """Return the current price."""
        now = datetime.now()
        season = get_season(now)
        period = get_period(now, season)
        return round(get_import_price(self._config_data, season, period), 6)
    
    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        now = datetime.now()
        season = get_season(now)
        period = get_period(now, season)
        return {
            "season": season,
            "period": period,
            "hour": now.hour,
        }


class HourlyPriceSensor(SensorEntity):
    """Sensor with hourly price forecast for next 24 hours."""
    
    def __init__(self, config_data, name):
        """Initialize the sensor."""
        self._config_data = config_data
        self._attr_name = name
        self._attr_native_unit_of_measurement = DEFAULT_UNIT_PRICE
        self._attr_icon = "mdi:chart-line"
        
    @property
    def native_value(self):
        """Return the current hour price."""
        now = datetime.now()
        season = get_season(now)
        period = get_period(now, season)
        return round(get_import_price(self._config_data, season, period), 6)
    
    @property
    def extra_state_attributes(self):
        """Return hourly forecast as attributes."""
        now = datetime.now()
        hourly_data = get_hourly_prices(self._config_data, now, hours=24)
        
        return {
            "hourly_prices": hourly_data,
            "forecast_hours": 24,
            "last_update": now.isoformat(),
        }


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
