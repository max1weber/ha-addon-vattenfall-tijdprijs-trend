# SPDX-License-Identifier: AGPL-3.0-only

from datetime import datetime, timedelta
import inspect
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
    entry_id = entry.entry_id

    sensors = [
        # Current price sensor
        CurrentPriceSensor(data, entry_id, "Huidige Importprijs", "import_price"),
        
        # Hourly forecast sensor
        HourlyPriceSensor(data, entry_id, "Importprijs per uur", "hourly_prices"),
        
        # Export sensors
        PriceSensor(entry_id, "Terugleververgoeding", data[CONF_EXPORT_COMPENSATION], DEFAULT_UNIT_PRICE, "export_compensation"),
        PriceSensor(entry_id, "Terugleverkosten", data[CONF_EXPORT_COSTS], DEFAULT_UNIT_PRICE, "export_costs"),

        # Fixed cost sensors
        FixedCostSensor(entry_id, "Vaste leveringskosten", data[CONF_FIXED_DELIVERY], "fixed_delivery"),
        FixedCostSensor(entry_id, "Vaste belastingvermindering", data[CONF_FIXED_TAX_REDUCTION], "fixed_tax_reduction"),
        FixedCostSensor(entry_id, "Vaste netbeheerkosten", data[CONF_FIXED_GRID], "fixed_grid"),
    ]

    result = async_add_entities(sensors)
    if inspect.isawaitable(result):
        await result


class CurrentPriceSensor(SensorEntity):
    """Sensor for current import price based on time-of-use."""
    
    _attr_should_poll = True
    
    def __init__(self, config_data, entry_id, name, sensor_type):
        """Initialize the sensor."""
        self._config_data = config_data
        self._entry_id = entry_id
        self._attr_name = name
        self._attr_unique_id = f"{entry_id}_{sensor_type}"
        self._attr_native_unit_of_measurement = DEFAULT_UNIT_PRICE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:currency-eur"
        self._attr_native_value = None
        self._attr_extra_state_attributes = {}
        
    @property
    def native_value(self):
        """Return the current price."""
        return self._attr_native_value
    
    async def async_update(self):
        """Update the sensor every minute."""
        now = datetime.now()
        season = get_season(now)
        period = get_period(now, season)
        self._attr_native_value = round(get_import_price(self._config_data, season, period), 6)
        self._attr_extra_state_attributes = {
            "season": season,
            "period": period,
            "hour": now.hour,
        }
    
    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        return self._attr_extra_state_attributes


class HourlyPriceSensor(SensorEntity):
    """Sensor with hourly price forecast for next 48 hours."""
    
    _attr_should_poll = True
    
    def __init__(self, config_data, entry_id, name, sensor_type):
        """Initialize the sensor."""
        self._config_data = config_data
        self._entry_id = entry_id
        self._attr_name = name
        self._attr_unique_id = f"{entry_id}_{sensor_type}"
        self._attr_native_unit_of_measurement = DEFAULT_UNIT_PRICE
        self._attr_icon = "mdi:chart-line"
        self._attr_native_value = None
        self._attr_extra_state_attributes = {}
        
    @property
    def native_value(self):
        """Return the current hour price."""
        return self._attr_native_value
    
    async def async_update(self):
        """Update hourly forecast every hour."""
        now = datetime.now()
        season = get_season(now)
        period = get_period(now, season)
        current_price = round(get_import_price(self._config_data, season, period), 6)
        self._attr_native_value = current_price
        
        # Update forecast data
        hourly_data = get_hourly_prices(self._config_data, now, hours=48)
        
        # Calculate median price for determining high/low tariffs
        prices = [entry["price"] for entry in hourly_data]
        sorted_prices = sorted(prices)
        median_price = sorted_prices[len(sorted_prices) // 2]
        
        # Format data for ApexCharts
        apexcharts_data = []
        apexcharts_data_colored = []
        for entry in hourly_data:
            price = entry["price"]
            # Color: green for low tariffs, red for high tariffs
            color = "#27ae60" if price <= median_price else "#e74c3c"

            # ApexCharts-card expects a list of [timestamp, value]
            apexcharts_data.append([entry["time"], round(price, 6)])

            # Optional richer format for custom cards/scripts
            apexcharts_data_colored.append({
                "x": entry["time"],
                "y": round(price, 6),
                "fillColor": color,
            })
        
        self._attr_extra_state_attributes = {
            "hourly_prices": hourly_data,
            "forecast_hours": 48,
            "last_update": now.isoformat(),
            "apexcharts_data": apexcharts_data,
            "apexcharts_data_colored": apexcharts_data_colored,
            "median_price": round(median_price, 6),
        }
    
    @property
    def extra_state_attributes(self):
        """Return hourly forecast as attributes."""
        return self._attr_extra_state_attributes


class PriceSensor(SensorEntity):
    def __init__(self, entry_id, name, value, unit, sensor_type):
        self._entry_id = entry_id
        self._attr_name = name
        self._attr_unique_id = f"{entry_id}_{sensor_type}"
        self._attr_native_value = value
        self._attr_native_unit_of_measurement = unit


class FixedCostSensor(SensorEntity):
    def __init__(self, entry_id, name, value, sensor_type):
        self._entry_id = entry_id
        self._attr_name = name
        self._attr_unique_id = f"{entry_id}_{sensor_type}"
        self._attr_native_value = value
        self._attr_native_unit_of_measurement = DEFAULT_UNIT_FIXED
