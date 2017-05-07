from shoelace.sensors import TemperatureSensor, GRSensor, HBSensor
import requests
import os
from shoelace.config import env

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

if (register_sensor(sensors)):
    val = 101
    print("VAL => ", val)
    temp_sens.push(val)
    val = 102
    print("VAL => ", val)
    temp_sens.push(val)
    val = 103
    print("VAL => ", val)
    temp_sens.push(val)
    val = 150
    print("VAL => ", val)
    temp_sens.push(val)
else:
    print("Try again later! >:|")

