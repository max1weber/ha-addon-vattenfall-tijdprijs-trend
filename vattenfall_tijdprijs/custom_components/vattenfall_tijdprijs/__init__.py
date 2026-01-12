# SPDX-License-Identifier: AGPL-3.0-only

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant


async def async_setup(hass: HomeAssistant, config: dict[str, Any]) -> bool:
    """Set up the Vattenfall Tijdprijs integration from YAML (not used)."""
    # This integration is configured via config entries only.
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Vattenfall Tijdprijs from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Vattenfall Tijdprijs config entry."""
    return await hass.config_entries.async_unload_platforms(entry, ["sensor"])
