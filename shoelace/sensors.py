from shoelace.core import Sensor
import requests
from shoelace.config import env
import math
import time

class TemperatureSensor(Sensor):
    """Temperature Sensor class
    Usage:
        >>> temp_sens = TemperatureSensor()
        >>> temp_sens.push(111)
    """
    @classmethod
    def limiar(cls):
        return 2

    def steinhart_hart(self, temp):
        print((float(temp)*5.0/(65535))*1.6/0.01)
        return (float(temp)*5.0/(65535))*1.6/0.01

    def push_callback(self, item):
        item = self.steinhart_hart(item)
        url = env["server_address"]+"/api/skin_temperatures"
        if (self.diff(item, self.last_sended) > TemperatureSensor.limiar()):
            item = int(item)
            self.last_sended = item
            is_critical = False
            if(item < 35 or item > 39):
                is_critical = True
            data = {
                'is_critical': is_critical,
                'temperature': item
            }
            r = requests.post(url, headers={'Authorization': 'Token '+self.token}, data=data)

        else:
            print("skip...")

class GRSensor(Sensor):
    """Galvanic Resistance Sensor class
    Usage:
        >>> grs = GRSensor()
        >>> grs.push(150)
    """
    @classmethod
    def limiar(cls):
        return 1 

    def normalize(self, item):
        if item <= 20:
            print("Disconnected")
            return 0 #Disconnected
        elif item >= 20 and item <=20000:
            print("NORMAL")
            return 1 #Normal status
        else:
            print("ALERT")
            return 2 #Alert status

    def push_callback(self, item):
        item = self.normalize(item)
        url = env["server_address"]+"/api/galvanic_resistances"
        if (self.last_sended != item):
            print("sending...")
            self.last_sended = item
            is_critical = False
            if(item == 2):
                is_critical = True
            data = {
                'is_critical': is_critical,
                'resistance': item
            }
            r = requests.post(url, headers={'Authorization': 'Token '+self.token}, data=data)
            print("R => ", r.json())
        else:
            print("skip...")

class HBSensor(Sensor):
    """HeartBeats Sensor class
    Usage:
        >>> hbs = HBSensor()
        >>> hbs.push(150)
    """
    @classmethod
    def limiar(cls):
        return 5

    def push_callback(self, item):
        url = env["server_address"]+"/api/heart_beats"
        if (self.diff(item, self.last_sended) > HBSensor.limiar()):
            print("sending...")
            self.last_sended = item
            data = {
                'beats': item
            }
            r = requests.post(url, headers={'Authorization': 'Token '+self.token}, data=data)
        else:
            print("skip...")

class FallSensor(Sensor):
    @classmethod
    def limiar(cls):
        return 5

    def normalize(self, item):
        if item > 10000:
            return 1
        else:
            return 0

    def push_callback(self, item):
        item = self.normalize(item)
        url = env["server_address"]+"/api/fellchair"
        if (item == 0 and self.last_sended == 1):
            print("sending...")
            r = requests.post(url, headers={'Authorization': 'Token '+self.token})
            #print(r)
        else:
            print("skip...")
        self.last_sended = item

class ECGSensor(Sensor):
    def __init__(self):
        self.rate = [0]*10
        self.sample_counter = 0
        self.last_beat_time = 0
        self.peak = 7300 # P
        self.trough = 7300 # T
        self.thresh = 7300
        self.amp = 100
        self.first_beat = True
        self.second_beat = False
        self.ibi = 600
        self.pulse = False
        self.last_time = int(time.time()*1000)
        self.bpm = 0

    @classmethod
    def limiar(cls):
        return 5

    def push_callback(self, item):
        url = env["server_address"]+"/api/heart_beats"
        current_time = int(time.time()*1000)
        self.sample_counter += current_time - self.last_time
        self.last_time = current_time
        n = self.sample_counter - self.last_beat_time
        if item < self.thresh and item < self.trough and n > (self.ibi/5.0)*3:
            self.trough = item

        if item > self.thresh and item > self.peak:
            self.peak = item

        if n > 250:                                 # avoid high frequency noise
            if item > self.thresh and self.pulse == False and n > (self.ibi/5.0)*3:
                self.pulse = True                        # set the Pulse flag when we think there is a pulse
                self.ibi = self.sample_counter - self.last_beat_time # measure time between beats in mS
                self.last_beat_time = self.sample_counter # keep track of time for next pulse

                if self.second_beat:                      # if this is the second beat, if secondBeat == TRUE
                    self.second_beat = False;             # clear secondBeat flag
                    for i in range(len(self.rate)):      # seed the running total to get a realisitic BPM at startup
                      self.rate[i] = self.ibi

                if self.first_beat:                       # if it's the first time we found a beat, if firstBeat == TRUE
                    self.first_beat = False;              # clear firstBeat flag
                    self.second_beat = True;              # set the second beat flag 
                    return

                # keep a running total of the last 10 IBI values
                self.rate[:-1] = self.rate[1:]                # shift data in the rate array
                self.rate[-1] = self.ibi # add the latest IBI to the rate array
                self.running_total = sum(self.rate)            # add upp oldest IBI values

                self.running_total /= len(self.rate)           # average the IBI values
                self.bpm = 60000/self.running_total # how many beats can fit into a minute? that's BPM!

        if item < self.thresh and self.pulse == True:       # when the values are going down, the beat is over
            self.pulse = False                           # reset the Pulse flag so we can do it again
            self.amp = self.peak - self.trough                             # get amplitude of the pulse wave
            self.thresh = self.amp/2 + self.trough                      # set thresh at 50% of the amplitude
            self.peak = self.thresh                              # reset these for next time
            self.trough = self.thresh

        if n > 2500:                                # if 2.5 seconds go by without a beat
            self.thresh = 7300                           # set thresh default
            self.peak = 7300                                # set P default
            self.trough = 7300                                # set T default
            self.last_beat_time = self.sample_counter # bring the lastBeatTime up to date
            self.first_beat = True                        # set these to avoid noise
            self.second_beat = False                      # when we get the heartbeat back
            self.bpm = 0

        if self.bpm > 0:
            print("BPM: %d" % self.bpm)
            data = {
                'beats': int(self.bpm)
            }
            r = requests.post(url, headers={'Authorization': 'Token '+self.token}, data=data)
            print(r.json())
        else:
            print("No heartbeat found")
