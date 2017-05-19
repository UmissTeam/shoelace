from shoelace.sensors import TemperatureSensor, GRSensor, HBSensor
import requests
import os
from shoelace.config import env
import time

TEST_ENVIRONMENT = False

try:
    import Adafruit_ADS1x15
except ImportError:
    TEST_ENVIRONMENT = True

def register_sensor(sensors):
    if (os.environ.get("UMISS_TOKEN") and os.environ.get("UMISS_PASSWORD")):
        login = os.environ["UMISS_TOKEN"]
        password = os.environ["UMISS_PASSWORD"]
        signup_url = env["server_address"]+"/api/monitors" # try to create user
        r = requests.post(signup_url, data={'username': login, 'password': password})
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

temp_sens = TemperatureSensor(TEST_ENVIRONMENT)
grs = GRSensor(TEST_ENVIRONMENT)
hbs = HBSensor(TEST_ENVIRONMENT)
sensors = [temp_sens, grs, hbs]

if (register_sensor(sensors)):
    while True:
        temp_sens.push(100)
        # THERM_READING = adc.read_adc(THERM_CHANNEL, gain=GAIN) #Reading values from the ADS
        # print(TEMPERATURE)
        time.sleep(0.5) #Pause for 0.5 second

else:
    print("Try again later! >:|")

