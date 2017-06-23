from abc import ABCMeta, abstractmethod
from collections import deque

class Sensor(metaclass=ABCMeta):
    """Sensor abstract class.
    To implement a new sensor, just:
        (i) inherit from Sensor class
        (ii) implement limiar and push_callback methods
    """
    def __init__(self):
        self.last_sended = 0

    @classmethod
    @abstractmethod
    def limiar(cls):
        pass

    @abstractmethod
    def push_callback(self, item):
        pass

    def diff(self, val1, val2):
        maxv = max(val1, val2)
        minv = min(val1, val2)
        return 100. - 100.*minv/maxv

    def push(self, item):
        self.push_callback(item)

