import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN
from .coordinator import XiaoDuCoordinator
from .xiaodu import XiaoDuHub

_LOGGER = logging.getLogger(__name__)

# 场景 解析为按钮
SUPPORT_TYPE = ['SCENE_TRIGGER']


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: XiaoDuCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities(parse_data(coordinator))


class XiaoDuScene(ButtonEntity):

    def press(self) -> None:
        hub: XiaoDuHub = self.hass.data[DOMAIN]['hub']
        hub.exec_scene(self.unique_id)

    def __init__(self, application_id, appliance_type, name_type, bot_id, bot_name) -> None:
        self._appliance_type = appliance_type
        self._attr_unique_id = application_id
        self._attr_name = name_type
        self.bot_id = bot_id
        self.bot_name = bot_name
        self._attr_icon = 'mdi:button-pointer'


def parse_data(coordinator: XiaoDuCoordinator) -> list[XiaoDuScene]:
    appliances = coordinator.data['data']['appliances']
    l: list[XiaoDuScene] = []
    if len(appliances) > 0:
        for app in appliances:
            appliance_type = app['applianceTypes'][0]
            if appliance_type in SUPPORT_TYPE:
                entity_id = app['applianceId'].replace('scene', 'thirdV1_scene')
                name_type = app['friendlyName']
                bot_id = app['botId']
                bot_name = app['botName']
                l.append(XiaoDuScene(entity_id, appliance_type, name_type, bot_id, bot_name))
    return l
