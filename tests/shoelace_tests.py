import unittest
from unittest import TestCase
from shoelace.sensors import Sensor, TemperatureSensor

class TestSensor(Sensor):
    @classmethod
    def limiar(cls):
        return 10

    @classmethod
    def maxitems(cls):
        return 5

    def alert_callback(self):
        self.critical_event = True
        self.alert_triggered = False

    def push_callback(self, item):
        pass

class ShoelaceTests(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_limiar_method(self):
        self.assertEqual(TestSensor.limiar(), 10.)

    def test_diff(self):
        test_sens = TestSensor()
        self.assertEqual(test_sens.diff(1, 2), 50.0)

    def test_list_execution_with_critical_event(self):
        test_sens = TestSensor()
        test_sens.critical_event = False
        test_sens.push(400.987)
        test_sens.push(400.987)
        test_sens.push(400.987)
        test_sens.push(400.987)
        test_sens.push(400.987)
        test_sens.push(400.987)
        test_sens.push(400.987)
        test_sens.push(400.987)
        test_sens.push(402.187)
        test_sens.push(406.987)
        test_sens.push(410.987)
        test_sens.push(420.987)
        self.assertEqual(test_sens.lowest_value, 400.987)
        self.assertEqual(test_sens.highest_value, 420.987)
        test_sens.push(1020.987)
        self.assertEqual(test_sens.critical_event, True)

    def test_list_execution_without_critical_event(self):
        test_sens = TestSensor()
        test_sens.critical_event = False
        test_sens.push(400.987)
        test_sens.push(401.987)
        test_sens.push(402.987)
        test_sens.push(403.987)
        test_sens.push(404.987)
        test_sens.push(405.987)
        test_sens.push(406.987)
        self.assertEqual(test_sens.critical_event, False)

if __name__ == '__main__':
        unittest.main()
