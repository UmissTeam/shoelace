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
        print((float(temp)*5.0/(65535))*1.6/0.01)
        return (float(temp)*5.0/(65535))*1.6/0.01

    def push_callback(self, item):
        item = self.steinhart_hart(item)
        url = env["server_address"]+"/api/skin_temperatures"
        if (self.diff(item, self.last_sended) > TemperatureSensor.limiar()):
            item = int(item)
            self.last_sended = item
            is_critical = False
            if(item < 35 or item > 39):
                is_critical = True
            data = {
                'is_critical': is_critical,
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
        return 1 

    def normalize(self, item):
        if item <= 20:
            print("Disconnected")
            return 0 #Disconnected
        elif item >= 20 and item <=210:
            print("NORMAL")
            return 1 #Normal status
        else:
            print("ALERT")
            return 2 #Alert status

    def push_callback(self, item):
        item = self.normalize(item)
        url = env["server_address"]+"/api/galvanic_resistances"
        if (self.last_sended != item):
            print("sending...")
            self.last_sended = item
            is_critical = False
            if(item == 2):
                is_critical = True
            data = {
                'is_critical': is_critical,
                'resistance': item
            }
            r = requests.post(url, headers={'Authorization': 'Token '+self.token}, data=data)
            print("R => ", r.json())
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
        if item > 10000:
            return 1
        else:
            return 0

    def push_callback(self, item):
        item = self.normalize(item)
        url = env["server_address"]+"/api/fellchair"
        if (item == 0 and self.last_sended == 1):
            print("sending...")
            #r = requests.post(url, headers={'Authorization': 'Token '+self.token})
            #print(r)
        else:
            print("skip...")
        self.last_sended = item
