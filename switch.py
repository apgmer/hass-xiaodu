import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.core import callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)
from .const import DOMAIN
from .coordinator import XiaoDuCoordinator
from .xiaodu import XiaoDuHub

_LOGGER = logging.getLogger(__name__)

# 开关 、 插座
SUPPORT_TYPE = ['SWITCH', 'OUTLET']


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: XiaoDuCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities(parse_data(coordinator))


class XiaoDuSwitch(CoordinatorEntity, SwitchEntity):

    def turn_on(self, **kwargs: Any) -> None:
        hub: XiaoDuHub = self.hass.data[DOMAIN]['hub']
        hub.switch_toggle(self._attr_unique_id, "TurnOnRequest")
        self._if_on = True

    def turn_off(self, **kwargs: Any) -> None:
        hub: XiaoDuHub = self.hass.data[DOMAIN]['hub']
        hub.switch_toggle(self._attr_unique_id, "TurnOffRequest")
        self._if_on = False

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self.hass.async_add_executor_job(self.turn_on)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.hass.async_add_executor_job(self.turn_off)
        await self.coordinator.async_request_refresh()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        appliances = self.coordinator.data['data']["appliances"]
        if len(appliances) > 0:
            for app in appliances:
                if self._attr_unique_id == app['applianceId']:
                    self._if_on = app['stateSetting']['turnOnState']['value'] == 'ON'
        self.async_write_ha_state()

    @property
    def is_on(self) -> bool | None:
        return self._if_on

    def __init__(self, coordinator, application_id, appliance_type, name_type, if_on, bot_id, bot_name) -> None:
        super().__init__(coordinator)
        self._appliance_type = appliance_type
        self._attr_unique_id = application_id
        self._attr_name = name_type
        self._if_on = if_on
        self.bot_id = bot_id
        self.bot_name = bot_name
        self._attr_icon = 'mdi:toggle-switch'
        self._attr_device_class = 'switch'
        if name_type and '灯' in name_type:
            self._attr_icon = 'mdi:lightbulb'
        if 'OUTLET' == appliance_type:
            self._attr_icon = 'mdi:power-socket-us'
            self._attr_device_class = 'outlet'


def parse_data(coordinator: XiaoDuCoordinator) -> list[XiaoDuSwitch]:
    appliances = coordinator.data['data']['appliances']
    l: list[XiaoDuSwitch] = []
    if len(appliances) > 0:
        for app in appliances:
            appliance_type = app['applianceTypes'][0]
            if appliance_type in SUPPORT_TYPE:
                entity_id = app['applianceId']
                if_on = app['stateSetting']['turnOnState']['value'] == 'ON'
                name_type = app['friendlyName']
                bot_id = app['botId']
                bot_name = app['botName']
                l.append(XiaoDuSwitch(coordinator, entity_id, appliance_type, name_type, if_on, bot_id, bot_name))
    return l
