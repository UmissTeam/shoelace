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

fall_samples_number = 10 #Number of samples to filter the average
fall_samples_delay = 1 #delay of 1 second between each measurement
fall_channel = 2 #ADS1115 Channel for the Fall Sensor

gsr_samples_number = 10 #Wait 10 samples of GSR to filter average
gsr_samples_delay = 0.02 #Time between samples equals to 20ms
gsr_channel = 1 #ADS1115 Channel for the GSR sensor

temperature_samples = 100 #Wait 100 samples to filter average
temperature_delay = 0.02 #delay 20 ms before taking a measurement
temperature_channel = 0 #ADS1115 Channel for the LM35 sensor

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

#-----------------------------FallSensor()----------------------------------------#
#Alert function for the fall sensor to detect if the user fell from the wheelchair#
#---------------------------------------------------------------------------------#
def FallSensor():
    fall_sum = 0.0 #Sum of the 10 samples in each loop
    for i in range(fall_samples_number):
        fall_adc_read = Adafruit_ADS1x15.ADS1115() #Read function for the ADS1115 ADC
        fall_value = fall_adc_read.read_adc(fall_channel, gain = GAIN) #Store value taken from the ADC
        fall_sum += fall_value
        time.sleep(fall_samples_delay)

    fall_avg = fall_sum/fall_samples_number #Average filter
    if fall_avg <= 50:#Calibration for the piezoelectric preassure sensor
        return 1 #Alert patient fall!
    else:
        return 0 #Normal status

#-------------------------------GRSensor()----------------------------------------#
#Alert function for the GSR sensor to detect the user stress level and skin status#
#---------------------------------------------------------------------------------#
def GRSensor():
    gsr_sum = 0.0
    for i in range(0, gsr_samples_number):
        gsr_adc_read = Adafruit_ADS1x15.ADS1115()
        gsr_value = gsr_adc_read.read_adc(gsr_channel, gain=GAIN)/100
        gsr_sum += gsr_value
        time.sleep(gsr_samples_delay) #delay

    gsr_avg = gsr_sum/gsr_samples_number #Filter average from gsr samples
    if gsr_avg <= 20:
        return 0 #Disconnected
    elif gsr_avg >= 20 and gsr_avg<=210:
        return 1 #Normal status
    else:
        return 2 #Alert status
    #print("GSR AVERAGE => ", gsr_avg)

#-----------------------------TemperatureSensor()--------------------------------#
#Function that returns the Temperature measurement in Celsius for the LM35 Sensor#
#--------------------------------------------------------------------------------#
def TemperatureSensor():
    lm35_adc_sum = 0.0
    for i in range(temperature_channel, temperature_samples):
        adc = Adafruit_ADS1x15.ADS1115()
        lm35_adc = adc.read_adc(0, gain=GAIN)
        lm35_adc_sum += lm35_adc
        time.sleep(temperature_delay)
    lm35_adc_avg = lm35_adc_sum/temperature_samples
    lm35_adc_sum = 0.0

    temp_celsius = (float(lm35_adc_avg)*5.0/(65535))/0.01
    #print("TEMPERATURA => ", "%.2f" %temp_celsius)
    return temp_celsius
