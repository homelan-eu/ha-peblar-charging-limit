"""Config flow for the homelan.eu Peblar Charging Limit integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import DOMAIN, PEBLAR_DOMAIN


class HomelanPeblarChargingLimitConfigFlow(ConfigFlow, domain=DOMAIN):
    """Confirm adding the integration; it needs no settings or credentials."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the confirmation step."""
        if not self.hass.config_entries.async_loaded_entries(PEBLAR_DOMAIN):
            return self.async_abort(reason="peblar_not_loaded")

        if user_input is not None:
            return self.async_create_entry(
                title="homelan.eu Peblar Charging Limit", data={}
            )

        return self.async_show_form(step_id="user", data_schema=vol.Schema({}))
