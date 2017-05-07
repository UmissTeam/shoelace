from shoelace.core import Sensor
import requests
from shoelace.config import env

class TemperatureSensor(Sensor):
    """Temperature Sensor class
    Usage:
        >>> temp_sens = TemperatureSensor()
        >>> temp_sens.push(111)
    """
    @classmethod
    def limiar(cls):
        return 5

    def push_callback(self, item):
        url = "http://localhost:8000/api/skin_temperatures"
        if (self.diff(item, self.last_sended) > TemperatureSensor.limiar()):
            print("sending...")
            self.last_sended = item
            data = {
                'temperature': item
            }
            r = requests.post(url, headers={'Authorization': 'Token '+self.token}, data=data)
        else:
            print("skip...")

class GRSensor(Sensor):
    """Galvanic Resistance Sensor class
    Usage:
        >>> grs = GRSensor()
        >>> grs.push(150)
    """
    @classmethod
    def limiar(cls):
        return 5

    def push_callback(self, item):
        url = "http://localhost:8000/api/galvanic_resistances"
        if (self.diff(item, self.last_sended) > GRSensor.limiar()):
            print("sending...")
            self.last_sended = item
            data = {
                'resistance': item
            }
            r = requests.post(url, headers={'Authorization': 'Token '+self.token}, data=data)
        else:
            print("skip...")

class HBSensor(Sensor):
    """HeartBeats Sensor class
    Usage:
        >>> hbs = HBSensor()
        >>> hbs.push(150)
    """
    @classmethod
    def limiar(cls):
        return 5

    def push_callback(self, item):
        url = "http://localhost:8000/api/heart_beats"
        if (self.diff(item, self.last_sended) > HBSensor.limiar()):
            print("sending...")
            self.last_sended = item
            data = {
                'beats': item
            }
            r = requests.post(url, headers={'Authorization': 'Token '+self.token}, data=data)
        else:
            print("skip...")
