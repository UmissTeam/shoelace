from shoelace.sensors import TemperatureSensor, GRSensor, HBSensor, FallSensor, ECGSensor
import requests
import os
from shoelace.config import env
import time
import math

TEST_ENVIRONMENT = False

try:
    import Adafruit_ADS1x15
except ImportError:
    TEST_ENVIRONMENT = True

def register_sensor(sensors):
    return True
    if (os.environ.get("UMISS_TOKEN") and os.environ.get("UMISS_PASSWORD")):
        login = "patient_7D23B6"
        password = os.environ["UMISS_PASSWORD"]
        signup_url = env["server_address"]+"/api/patients" # try to create user
        r = requests.post(signup_url, data={'username': login, 'password': password, 'token': os.environ["UMISS_TOKEN"]})
        print(r.json())
        login_url = env["server_address"]+"/api-auth-token/" # try to login user
        r = requests.post(login_url, data={'username': login, 'password': password})
        for u in sensors:
            u.token = r.json()["token"] # pass token to sensor
        if (temp_sens.token):
            return True
        else:
            return False
    else:
        print("Missing tokens")

temp_sens = TemperatureSensor()
grs = GRSensor()
fall = FallSensor()
ecg = ECGSensor()
sensors = [temp_sens, grs, fall, ecg]

adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

def collect_temperature_sensor():
    temperature_samples = 100
    lm35_adc_sum = 0.0
    for i in range(0, temperature_samples):
        lm35_adc = adc.read_adc(0, gain=GAIN)
        lm35_adc_sum += lm35_adc
    lm35_adc_avg = lm35_adc_sum/temperature_samples
    return lm35_adc_avg


def collect_fall_sensor():
    fall_sum = 0.0
    samples = 10
    fall_sum = 0.0
    for i in range(0, samples):
        fall_value = adc.read_adc(2, gain = GAIN)
        fall_sum += fall_value
    return fall_sum/samples


def collect_gsr_sensor():
    samples = 10
    gsr_sum = 0.0
    for i in range(0, samples):
        gsr_value = adc.read_adc(1, gain=GAIN)/100.
        gsr_sum += gsr_value
    return gsr_sum/samples #Filter average from gsr samples


def collect_ecg_sensor():
    return adc.read_adc(3, gain=2/3)

if (register_sensor(sensors)):
    while True:
        sensors[0].push(collect_temperature_sensor()) # 0
        # sensors[1].push(collect_gsr_sensor()) # 1
        # sensors[2].push(collect_fall_sensor()) # 2
        # sensors[3].push(collect_ecg_sensor()) # 3
else:
    print("Try again later! >:|")
