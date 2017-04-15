from abc import ABCMeta, abstractmethod
from collections import deque

class Sensor(metaclass=ABCMeta):
    """Sensor abstract class.
    To implement a new sensor, just:
        (i) inherit from Sensor class
        (ii) implement limiar, maxitems, push_callback and alert_callback methods
    OBS: set alert_triggered attribute to False inside alert_callback!!!
    """
    def __init__(self):
        self.collection = deque()
        self.lowest_value = 0xffffff
        self.highest_value = -1
        self.alert_triggered = False

    @classmethod
    @abstractmethod
    def maxitems(cls):
        pass

    @classmethod
    @abstractmethod
    def limiar(cls):
        pass

    def alert(self):
        while (self.alert_triggered == True):
            self.alert_callback()

    @abstractmethod
    def alert_callback(self):
        pass

    @abstractmethod
    def push_callback(self, item):
        pass

    def diff(self, val1, val2):
        maxv = max(val1, val2)
        minv = min(val1, val2)
        return 100. - 100.*minv/maxv

    def push(self, item):
        self.lowest_value = min(self.lowest_value, item)
        self.highest_value = max(self.highest_value, item)
        self.push_callback(item)
        if (len(self.collection) > self.maxitems()):
            diff1 = self.diff(self.lowest_value, item)
            diff2 = self.diff(self.highest_value, item)
            if ((diff1 > self.limiar()) or (diff2 > self.limiar())):
                self.alert_triggered = True
                self.alert()
            self.collection.popleft()
        self.collection.append(item)

