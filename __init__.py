"""The xiaodu api integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .coordinator import XiaoDuCoordinator
from .xiaodu import XiaoDuHub

_LOGGER = logging.getLogger(__name__)

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS: list[Platform] = [Platform.SWITCH, Platform.COVER, Platform.BUTTON]


async def async_setup_entry(hass, entry):
    """Set up xiaodu api from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    # TODO 1. Create API instance
    # TODO 2. Validate the API connection (and authentication)
    # TODO 3. Store an API object for your platforms to access
    # hass.data[DOMAIN][entry.entry_id] = MyApi(...)

    hub = XiaoDuHub(entry.data['cookie'], hass)

    coordinator = XiaoDuCoordinator(hass, hub)
    hass.data[DOMAIN][entry.entry_id] = coordinator

    hass.data[DOMAIN]['hub'] = hub

    # await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(
        entry, [platform for platform in PLATFORMS if platform != Platform.NOTIFY]
    )

    # job_ = await hass.async_add_executor_job()
    # print("")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
