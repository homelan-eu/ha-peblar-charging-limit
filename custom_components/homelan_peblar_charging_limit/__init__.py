"""Expose the Peblar user-defined charging limit in Home Assistant.

This integration adds to the built-in Peblar integration and reuses its
logged-in session, so it stores no credentials of its own. It can be removed
once the built-in integration offers this setting itself.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.config_entries import ConfigEntry, ConfigEntryState
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import ConfigEntryError, ConfigEntryNotReady
from homeassistant.helpers import device_registry as dr

from .const import PEBLAR_DOMAIN

PLATFORMS = [Platform.NUMBER]


@dataclass(slots=True)
class PeblarLink:
    """The parts of the built-in Peblar integration used here."""

    coordinator: Any
    device: dr.DeviceEntry
    hardware_max_current: int
    serial_number: str


type HomelanPeblarConfigEntry = ConfigEntry[PeblarLink]


def _build_link(hass: HomeAssistant, peblar_entry: ConfigEntry) -> PeblarLink:
    """Read and check the internals this integration depends on."""
    runtime_data = peblar_entry.runtime_data
    coordinator = runtime_data.user_configuration_coordinator
    system_information = runtime_data.system_information

    # Touch every attribute now, so a Home Assistant update that changes them
    # fails once with a clear message instead of on every state update.
    _ = coordinator.peblar
    configuration = coordinator.data
    _ = configuration.user_defined_charge_limit_current
    _ = configuration.user_defined_charge_limit_current_allowed
    _ = configuration.current_control_fixed_charge_current_limit

    # Device identifiers are scoped per config entry, so look up the device
    # that belongs to the built-in Peblar integration's own config entry.
    serial_number = system_information.product_serial_number
    device = next(
        (
            device
            for device in dr.async_entries_for_config_entry(
                dr.async_get(hass), peblar_entry.entry_id
            )
            if (PEBLAR_DOMAIN, serial_number) in device.identifiers
        ),
        None,
    )
    if device is None:
        raise ConfigEntryError("The Peblar device was not found")

    return PeblarLink(
        coordinator=coordinator,
        device=device,
        hardware_max_current=system_information.hardware_max_current,
        serial_number=serial_number,
    )


async def async_setup_entry(
    hass: HomeAssistant, entry: HomelanPeblarConfigEntry
) -> bool:
    """Set up the charging limit on top of the built-in Peblar integration."""
    peblar_entries = hass.config_entries.async_loaded_entries(PEBLAR_DOMAIN)
    if not peblar_entries:
        raise ConfigEntryNotReady("The Peblar integration is not loaded yet")
    peblar_entry = peblar_entries[0]

    try:
        entry.runtime_data = _build_link(hass, peblar_entry)
    except AttributeError as err:
        raise ConfigEntryError(
            "The built-in Peblar integration has changed and is no longer "
            f"compatible with this custom integration (missing: {err.name})"
        ) from None

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    reload_scheduled = False

    @callback
    def _async_peblar_state_changed() -> None:
        """Reload when Peblar unloads, because its session is replaced."""
        nonlocal reload_scheduled
        if reload_scheduled or peblar_entry.state is ConfigEntryState.LOADED:
            return
        reload_scheduled = True
        hass.config_entries.async_schedule_reload(entry.entry_id)

    entry.async_on_unload(
        peblar_entry.async_on_state_change(_async_peblar_state_changed)
    )
    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: HomelanPeblarConfigEntry
) -> bool:
    """Unload the integration."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
