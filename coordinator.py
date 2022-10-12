from __future__ import annotations

import logging
from datetime import timedelta

import async_timeout

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)
from .xiaodu import XiaoDuHub

_LOGGER = logging.getLogger(__name__)


class XiaoDuCoordinator(DataUpdateCoordinator):

    def __init__(self, hass: HomeAssistant, hub: XiaoDuHub):
        super().__init__(
            hass,
            _LOGGER,
            name="xiaodu api",
            update_interval=timedelta(seconds=10),
        )
        self.hub = hub

    async def _async_update_data(self):
        async with async_timeout.timeout(10):
            return await self.hub.deviceList()
