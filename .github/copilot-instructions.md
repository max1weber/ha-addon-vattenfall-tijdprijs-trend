# GitHub Copilot Instructions for Vattenfall Tijdprijs Home Assistant Integration

## Project Overview

This is a Home Assistant custom integration for Vattenfall TijdPrijs dynamic energy pricing in the Netherlands. The integration calculates energy import/export prices based on:
- Time-of-use periods (summer/winter, normal/off-peak)
- Fixed daily costs (delivery, tax reduction, grid management)
- Export compensation and costs for returned electricity

**Domain**: `vattenfall_tijdprijs`  
**Current Version**: 1.1.0  
**License**: AGPL-3.0-only  
**Language**: Python 3.x  
**Framework**: Home Assistant Core

## Code Structure

```
custom_components/vattenfall_tijdprijs/
├── __init__.py           # Integration initialization (minimal)
├── config_flow.py        # Configuration flow for setup wizard
├── const.py              # All constants and configuration keys
├── manifest.json         # Integration metadata
├── pricing_data.py       # Pricing calculation logic and tier management
├── sensor.py             # Sensor entity definitions
├── strings.json          # UI strings for config flow
└── translations/         # Localization files
    └── en.json
tests/                    # Test suite
├── conftest.py           # Pytest fixtures
├── test_config_flow.py   # Config flow tests
├── test_pricing_data.py  # Pricing logic tests
└── test_sensor.py        # Sensor entity tests
```

## Coding Standards

### General Guidelines

1. **SPDX License Header**: All Python files MUST start with:
   ```python
   # SPDX-License-Identifier: AGPL-3.0-only
   ```

2. **Docstrings**: Use triple-quoted strings for module and function documentation
   ```python
   """Brief description of the module or function."""
   ```

3. **Type Hints**: Prefer type hints where appropriate, especially for function parameters and return values
   ```python
   def get_tier_index(annual_consumption_kwh: float) -> int:
   ```

4. **Constants**: Define all constants in `const.py`, use UPPERCASE naming
   ```python
   DEFAULT_FIXED_DELIVERY = 0.295572
   CONF_ANNUAL_CONSUMPTION = "annual_consumption"
   ```

5. **Imports**: Use absolute imports from Home Assistant and local modules
   ```python
   from homeassistant.components.sensor import SensorEntity
   from .const import DOMAIN, DEFAULT_UNIT_PRICE
   ```

### Home Assistant Specific

1. **Config Flow**: Use the Home Assistant config flow pattern for user configuration
   - Multi-step flows with clear step names
   - Default values for all optional fields
   - Input validation using `vol.Schema`

2. **Sensor Entities**: 
   - Inherit from `SensorEntity`
   - Use `_attr_name` and `_attr_native_value` for properties
   - Set `_attr_native_unit_of_measurement` appropriately (€/kWh or €/dag)

3. **Async Functions**: Use `async` for setup functions
   ```python
   async def async_setup_entry(hass, entry, async_add_entities):
   ```

4. **Entity IDs**: Follow pattern `sensor.vattenfall_tijdprijs_*`

### Pricing Logic

1. **Price Components**:
   - **Belasting** (tax): Fixed energy tax, same for all periods
   - **Levering** (delivery): Varies by period, configurable
   - **Total import price** = Levering + Belasting

2. **Seasons**:
   - Summer: April-September
   - Winter: October-March

3. **Time Periods** (defined in `TOU_PERIODS` in `const.py`):
   - Summer: normal, off_peak_weekday, off_peak_weekend
   - Winter: normal, off_peak_day, off_peak_night

4. **Currency**: All prices in EUR (€), inclusive of 21% VAT

### Testing

1. **Test Framework**: Use `pytest` with `pytest-asyncio` for async tests

2. **Coverage**: Aim for high test coverage (current project uses codecov)

3. **Fixtures**: Define common fixtures in `tests/conftest.py`

4. **Test Structure**:
   - Test config flow steps and validation
   - Test pricing calculations for all tiers and periods
   - Test sensor entity creation and values

5. **Run Tests**:
   ```bash
   pytest tests/ --cov=custom_components/vattenfall_tijdprijs --cov-report=xml
   ```

## Configuration Schema

The integration uses a multi-step configuration flow:

1. **Annual Consumption**: Enter annual consumption value in kWh (determines pricing tier)
2. **Fixed Costs**: Daily delivery costs, tax reduction, grid costs
3. **Delivery Tariffs** (optional): Configure levering prices per period/tier
4. **Export Tariffs**: Compensation and costs for returned electricity

All configuration values are stored in `entry.data` dictionary with keys defined in `const.py` (CONF_* constants).
Fixed Costs**: Daily delivery costs, tax reduction, grid costs
2. **Delivery Tariffs** (optional): Configure levering prices per period
3. **Export Tariffs**: Compensation and costs for returned electricity

All configuration values are stored in `entry.data` dictionary with keys defined in `const.py` (CONF_* constants).

### Future Enhancements (Post v1.1.0)

- **Consumption Sensor Integration**: Ability to link to an existing Home Assistant sensor for automatic annual consumption tracking
- **Usage Tier Pricing**: Dynamic pricing based on annual consumption tiers (0-2900, 2900-10000, 10000-50000, 50000+ kWh)
2. Set appropriate `_attr_*` properties
3. Add to the sensors list in `async_setup_entry`
4. Add corresponding configuration keys to `const.py` if needed
5. Update `strings.json` for UI labels
6. Write tests in `test_sensor.py`

### Modifying Pricing Logic

1. Update `BELASTING` or `DEFAULT_LEVERING_PRICES` in `pricing_data.py`
2. Adjust calculation function (`get_import_price`)
3. Update corresponding tests in `test_pricing_data.py`
4. Update README.md if default values change

### Adding Configuration Options

1. Add constant to `const.py` (CONF_* for keys, DEFAULT_* for defaults)
2. Add to config flow schema in `config_flow.py`
3. Add UI strings to `strings.json` and `translations/en.json`
4. Update sensor or pricing logic to use new configuration
5. Add tests for validation and usage

## Dutch Context

This integration is primarily for Dutch users:
- Primary language is Dutch (NL)
- Currency is EUR (€)
- Energy units: kWh
- Date format: European (day/month/year)
- All user-facing strings should be in Dutch in `strings.json`
- English translations in `translations/en.json` for international users

## Dependencies

- **Runtime**: No external dependencies (pure Home Assistant integration)
- **Development**:
  - pytest >= 7.0
  - pytest-cov >= 4.0
  - pytest-asyncio >= 0.20.0
  - homeassistant >= 2023.1.0
  - voluptuous >= 0.13.1

## Important Notes

1. **No External API Calls**: This is a calculated integration (`iot_class: calculated`), it does not make external API calls
2. **State Management**: All pricing data is calculated from configuration, not fetched dynamically
3. **Version Sync**: Keep version number consistent across:
   - `const.py` (VERSION)
   - `manifest.json` (version)
   - README.md badges (if applicable)
4. **HACS Compatible**: Ensure changes maintain HACS compatibility
5. **Backwards Compatibility**: Consider migration paths when changing config schema

## When Making Changes

1. Always add/update tests for new functionality
2. Update README.md if user-facing features change
3. Update both Dutch and English strings
4. Run full test suite before committing
5. Follow semantic versioning (MAJOR.MINOR.PATCH)
6. Update `manifest.json` version when releasing
7. Ensure SPDX license header is present in all new files
8. Consider impact on existing user configurations

## Code Review Checklist

- [ ] SPDX license header present
- [ ] Type hints used appropriately
- [ ] Constants defined in `const.py`
- [ ] Docstrings for public functions
- [ ] Tests written and passing
- [ ] Dutch and English strings updated
- [ ] No external dependencies added (unless necessary)
- [ ] Follows Home Assistant integration best practices
- [ ] Version numbers updated if needed
- [ ] README.md reflects changes
