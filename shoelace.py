from shoelace.sensors import TemperatureSensor, GRSensor, HBSensor
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

temp_sens = TemperatureSensor()
grs = GRSensor()
hbs = HBSensor()
sensors = [temp_sens, grs, hbs]

adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

if (register_sensor(sensors)):
    while True:
        therm = adc.read_adc(0, gain=GAIN)
        volts = (therm * 3.3) / 65536.
        ohms = ((volts)*3300.)-1000.
        print("OHMS => ", ohms)
        lnohm = math.log1p(ohms)
        a = 0.001129148 #STEINHART-HART A coefficient
        b = 0.000234125 #STEINHART-HART B coefficient
        c = 0.0000000876741 #STEINHART-HART C coefficient
        t1 = (b*lnohm) 
        t2 = math.pow(lnohm,3)
        t2 *= c
        temp = 1./(a + t1 + t2)
        tempc = temp - 273.15 - 66.2
        print ("%4d/1023 => %5.3f V => %4.1f Ω => %4.1f °K => %4.1f °C from adc" % (therm, volts, ohms, temp, tempc))
        temp_sens.push(tempc)
        time.sleep(0.5) #Pause for 0.5 second

else:
    print("Try again later! >:|")

