"""Number entity for the Peblar user-defined charging limit."""

from __future__ import annotations

from typing import Any

from peblar import PeblarSetUserConfiguration

from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberMode,
)
from homeassistant.const import EntityCategory, UnitOfElectricCurrent
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import HomelanPeblarConfigEntry, PeblarLink
from .const import MINIMUM_CHARGE_LIMIT


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HomelanPeblarConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add the charging limit entity."""
    async_add_entities([HomelanPeblarChargingLimitNumber(entry.runtime_data)])


class HomelanPeblarChargingLimitNumber(CoordinatorEntity[Any], NumberEntity):
    """The limit shown at the top of the charger's Smart Charging page."""

    _attr_device_class = NumberDeviceClass.CURRENT
    _attr_entity_category = EntityCategory.CONFIG
    _attr_has_entity_name = True
    _attr_mode = NumberMode.SLIDER
    _attr_name = "User charge limit (homelan.eu)"
    _attr_native_min_value = MINIMUM_CHARGE_LIMIT
    _attr_native_step = 1
    _attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE

    def __init__(self, link: PeblarLink) -> None:
        """Initialize the entity."""
        super().__init__(link.coordinator)
        self._hardware_max_current = link.hardware_max_current
        self._attr_unique_id = (
            f"{link.serial_number}_homelan_user_defined_charge_limit"
        )
        # Show the entity on the device of the built-in Peblar integration.
        self.device_entry = link.device

    @property
    def available(self) -> bool:
        """Return whether this limit can be changed within the safe range."""
        return (
            super().available
            and self.coordinator.data.user_defined_charge_limit_current_allowed
            and self.native_max_value >= MINIMUM_CHARGE_LIMIT
        )

    @property
    def native_max_value(self) -> float:
        """Follow the installation limit, within the charger's hardware rating."""
        return min(
            self._hardware_max_current,
            self.coordinator.data.current_control_fixed_charge_current_limit,
        )

    @property
    def native_value(self) -> int:
        """Return the current user-defined charging limit."""
        return self.coordinator.data.user_defined_charge_limit_current

    async def async_set_native_value(self, value: float) -> None:
        """Write the new user-defined charging limit to the charger."""
        try:
            await self.coordinator.peblar.update_user_configuration(
                PeblarSetUserConfiguration(
                    user_defined_charge_limit_current=int(value)
                )
            )
        except Exception as err:  # noqa: BLE001
            # Report only the error type and drop the original exception: its
            # message can contain text from the charger's response.
            raise HomeAssistantError(
                f"Could not set the Peblar charging limit ({type(err).__name__})"
            ) from None
        await self.coordinator.async_request_refresh()
