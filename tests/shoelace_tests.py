import unittest
from unittest import TestCase
from shoelace.sensors import Sensor, TemperatureSensor

class TestSensor(Sensor):
    @classmethod
    def limiar(cls):
        return 1

    def push_callback(self, item):
        if (self.diff(item, self.last_sended) > TestSensor.limiar()):
            self.last_sended = item


class ShoelaceTests(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_limiar_method(self):
        self.assertEqual(TestSensor.limiar(), 1.)

    def test_diff(self):
        test_sens = TestSensor()
        self.assertEqual(test_sens.diff(1, 2), 50.0)

    def test_list_last_sended(self):
        test_sens = TestSensor()
        test_sens.push(400.987)
        self.assertEqual(test_sens.last_sended, 400.987)
        test_sens.push(400.989)
        self.assertEqual(test_sens.last_sended, 400.987)
        test_sens.push(402.187)
        test_sens.push(406.987)
        test_sens.push(410.987)
        test_sens.push(420.987)

if __name__ == '__main__':
        unittest.main()
