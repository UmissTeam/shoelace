from shoelace.core import Sensor
import requests
from shoelace.config import env

class TemperatureSensor(Sensor):
    """Temperature Sensor class
    Usage:
        >>> temp_sens = TemperatureSensor()
        >>> temp_sens.push(2)
    """
    @classmethod
    def limiar(cls):
        return 5

    @classmethod
    def maxitems(cls):
        return 20

    def alert_callback(self):
        self.alert_triggered = False

    def push_callback(self, item):
        url = env['server_address'] + '/components'
        data = {
            'data': {
                'location': {
                    "value": [-23.557620375, -46.735339374999995],
                    "timestamp": "2017-04-15T16:03:02-03:00",
                    "bus_id": "82409"
                }
            },
            "id": "2a50ed17-2a7e-4db3-9af6-f9b9b9cd6afd"
        }
        print("DATA => ", data)
        requests.post(url, data=data)
