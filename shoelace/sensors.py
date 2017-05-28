from shoelace.core import Sensor
import requests
from shoelace.config import env
import math

class TemperatureSensor(Sensor):
    """Temperature Sensor class
    Usage:
        >>> temp_sens = TemperatureSensor()
        >>> temp_sens.push(111)
    """
    @classmethod
    def limiar(cls):
        return 2

    def steinhart_hart(self, temp):
        return (float(temp)*5.0/(65535))/0.01

    def push_callback(self, item):
        item = self.steinhart_hart(item)
        url = env["server_address"]+"/api/skin_temperatures"
        if (self.diff(item, self.last_sended) > TemperatureSensor.limiar()):
            item = int(item)
            self.last_sended = item
            data = {
                'temperature': item
            }
            r = requests.post(url, headers={'Authorization': 'Token '+self.token}, data=data)
            print(r.json())
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
        return 0

    def normalize(self, item):
        if item <= 20:
            return 0 #Disconnected
        elif item >= 20 and item <=210:
            return 1 #Normal status
        else:
            return 2 #Alert status

    def push_callback(self, item):
        item = self.normalize(item)
        url = env["server_address"]+"/api/galvanic_resistances"
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
        url = env["server_address"]+"/api/heart_beats"
        if (self.diff(item, self.last_sended) > HBSensor.limiar()):
            print("sending...")
            self.last_sended = item
            data = {
                'beats': item
            }
            r = requests.post(url, headers={'Authorization': 'Token '+self.token}, data=data)
        else:
            print("skip...")

class FallSensor(Sensor):
    @classmethod
    def limiar(cls):
        return 5

    def normalize(self, item):
        if item <= 50:
            return 1
        else:
            return 0

    def push_callback(self, item):
        item = self.normalize(item)
        # url = env["server_address"]+"/api/heart_beats"
        # if (self.diff(item, self.last_sended) > HBSensor.limiar()):
        #     print("sending...")
        #     self.last_sended = item
        #     data = {
        #         'beats': item
        #     }
        #     r = requests.post(url, headers={'Authorization': 'Token '+self.token}, data=data)
        # else:
        #     print("skip...")
