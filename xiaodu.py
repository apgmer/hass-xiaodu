import logging

import requests

HOST = 'https://xiaodu.baidu.com'

_LOGGER = logging.getLogger(__name__)


class XiaoDuHub:

    def __init__(self, cookie: str, hass) -> None:
        self.cookie = cookie
        self._hass = hass
        self._device_dict = None

    async def auth(self) -> bool:
        return True

    async def deviceList(self):
        return await self._hass.async_add_executor_job(self.doDeviceList)

    def doDeviceList(self):
        api = '/saiya/smarthome/devicelist?from=h5_control&withscene=1&generalscene=3'
        headers = self._common_header()
        _LOGGER.info("do query xiaodu device")
        response = requests.get(HOST + api, headers=headers)
        if response.status_code == 200:
            json = response.json()
            _LOGGER.info("request \n %s \n %s \n %s \t %s", HOST + api, '', response.status_code, response.json())
            return json
        else:
            _LOGGER.error("请求小度出错", response)
            return {}

    def switch_toggle(self, unique_id, method):
        api = '/saiya/smarthome/directivesend?from=h5_control'
        param = {
            "header": {
                "namespace": "DuerOS.ConnectedHome.Control",
                "name": method,
                "payloadVersion": 3
            },
            "payload": {
                "appliance": {
                    "applianceId": [
                        unique_id
                    ]
                },
                "parameters": {
                    "proxyConnectStatus": False
                }
            }
        }
        response = requests.post(HOST + api, headers=self._common_header(), json=param)
        _LOGGER.info("request \n %s \n %s \n %s \t %s", HOST + api, param, response.status_code, response.json())
        return response.status_code == 200

    # 厂商无效果
    def curtain_set_position(self, unique_id, position: int):
        api = '/saiya/smarthome/directivesend?from=h5_control'
        param = {
            "header": {
                "namespace": "DuerOS.ConnectedHome.Control",
                "name": "TurnOnPercentRequest",
                "payloadVersion": 3
            },
            "payload": {
                "appliance":
                    {"applianceId":
                         [unique_id]
                     },
                "degree": position,
                "parameters": {
                    "attribute": "degree",
                    "attributeValue": str(position),
                    "proxyConnectStatus": False
                }
            }
        }
        response = requests.post(HOST + api, headers=self._common_header(), json=param)
        _LOGGER.info("request \n %s \n %s \n %s \t %s", HOST + api, param, response.status_code, response.json())
        return response.status_code == 200

    def curtain_toggle(self, unique_id, method):
        api = '/saiya/smarthome/directivesend?from=h5_control'
        param = {
            "header": {
                "namespace": "DuerOS.ConnectedHome.Control",
                "name": method,
                "payloadVersion": 3
            },
            "payload": {
                "appliance": {
                    "applianceId": [
                        unique_id
                    ]
                },
                "parameters": {
                    "proxyConnectStatus": False
                }
            }
        }
        response = requests.post(HOST + api, headers=self._common_header(), json=param)
        _LOGGER.info("request \n %s \n %s \n %s \t %s", HOST + api, param, response.status_code, response.json())
        return response.status_code == 200


    def curtain_stop(self, unique_id):
        api = '/saiya/smarthome/directivesend?from=h5_control'
        param = {
            "header": {
                "namespace": "DuerOS.ConnectedHome.Control",
                "name": "PauseRequest",
                "payloadVersion": 3
            },
            "payload": {
                "appliance": {
                    "applianceId": [
                        unique_id
                    ]
                },
                "parameters": {
                    "proxyConnectStatus": False
                }
            }
        }
        response = requests.post(HOST + api, headers=self._common_header(), json=param)
        _LOGGER.info("request \n %s \n %s \n %s \t %s", HOST + api, param, response.status_code, response.json())
        return response.status_code == 200

    def exec_scene(self, unique_id):
        api = '/saiya/smarthome/unified'
        param = {"method": "triggerScene", "params": {"sceneId": unique_id}}
        response = requests.post(HOST + api, headers=self._common_header(), json=param)
        _LOGGER.info("request \n %s \n %s \n %s \t %s", HOST + api, param, response.status_code, response.json())
        return response.status_code == 200

    def _common_header(self):
        return {
            "Cookie": self.cookie,
            "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            "Referer": 'https://xiaodu.baidu.com/saiya/smarthome/index.html?uid=&traceid='
        }
