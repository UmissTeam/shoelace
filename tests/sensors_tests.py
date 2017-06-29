import pytest
from shoelace.sensors import ECGSensor
import time


@pytest.fixture
def ecg():
    return ECGSensor()

def test_ecg_values(ecg):
    assert ecg.bpm == 0
    ecg.push(10000)
    ecg.push(10000)
    ecg.push(10000)
    ecg.push(10000)
    ecg.push(10000)
    ecg.push(10000)
    ecg.push(500)
    ecg.push(50)
    ecg.push(50)
    ecg.push(50)
    ecg.push(50)
    assert ecg.bpm != 0

