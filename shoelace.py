from shoelace.sensors import TemperatureSensor, GRSensor, HBSensor
import requests
import os
from shoelace.config import env
import Adafruit_ADS1x15

def register_sensor(sensors):
    if (os.environ.get("UMISS_TOKEN") and os.environ.get("UMISS_PASSWORD")):
        login = os.environ["UMISS_TOKEN"]
        password = os.environ["UMISS_PASSWORD"]
        signup_url = env["server_address"]+"/api/users" # try to create user
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

THERM_CHANNEL = 0 #Thermistor ADS Channel
SERIES_RESISTANCE = 10000 #Series resistance from the circuit
ADS_RESOLUTION = 65536 # ADC 16 bits resolution (2**16)
GAIN = 1 #Read voltages between -4.096 and +4.096
THERM_A = 0.001129148 #STEINHART-HART A coefficient
THERM_B = 0.000234125 #STEINHART-HART B coefficient
THERM_C = 0.0000000876741 #STEINHART-HART C coefficient

if (register_sensor(sensors)):
    while True:
        THERM_READING = adc.read_adc(THERM_CHANNEL, gain=GAIN) #Reading values from the ADS
        THERM_RESISTANCE = ((ADS_RESOLUTION/THERM_READING) - SERIES_RESISTANCE) #Calculates the Thermistor resistance
        TEMPERATURE = math.log(THERM_RESISTANCE)
        TEMPERATURE = 1 / (THERM_A + (THERM_B * TEMPERATURE) + (THERM_C * TEMPERATURE * TEMPERATURE * TEMPERATURE))

        TEMPERATURE = TEMPERATURE - 273.15 #Convert Kelvin to Celsius
        print(TEMPERATURE)
        time.sleep(0.5) #Pause for 0.5 second

else:
    print("Try again later! >:|")

