
import requests
from pandas import json_normalize
import time
import numpy as np

from colorama import Style
from colorama import Fore
from colorama import init as colorama_init

colorama_init()


def sendSensorData(name, value):
    # sensor place holder
    sensor_name = name
    sensor_value = value
    sensor_id = 'device6ef0e2a6f88f481ea81e388d8be91a1c'

    # request parameters
    device_id = 'device6ef0e2a6f88f481ea81e388d8be91a1c'
    base_url = 'https://connect.forge-api.com'
    body = {
        "sensor_data": {
            'sensor_name': sensor_name,
            'sensor_value': sensor_value,
            'sensor_id': sensor_id,
        },
        "device_id": device_id,
    }
    headers = {'User-Agent': 'XY', 'Content-type': 'application/json'}
    response = requests.post(f"{base_url}/devices", json=body, headers=headers, params={
        "device_id": device_id,
    })
    data = response.json()

    json_normalize(data)
    return data


class sensor:
    def __init__(self, name=''):
        self.name = name
        self.samples = None
        self.index = 0
        self.device_id = None
        self.sensor_name = None
        self.sensor_value = None
        self.sleep = 1

    def authenticate(self, device_id):
        # authenticate
        self.device_id = device_id
        return self

    def createSamples(start_temperature, end_temperature, amount):
        arr = np.linspace(start_temperature, end_temperature, amount)
        def roundVal(val): return round(val, 1)
        applyall = np.vectorize(roundVal)(arr)
        return applyall

    def send(self, dict={}):
        self.sensor_name = list(dict.keys())[0]
        self.sensor_value = round(dict[self.sensor_name], 1)

        # delay after sending
        time.sleep(self.sleep)

        print(
            f"{Fore.LIGHTMAGENTA_EX}[sensor]{Style.RESET_ALL} sent {Fore.LIGHTBLUE_EX}{self.sensor_name}{Style.RESET_ALL} value of {Fore.YELLOW}{self.sensor_value}°F {Style.RESET_ALL}to remote")
        if self.device_id is not None:
            sendSensorData(self.sensor_name, self.sensor_value)
        else:
            print("Device id not authenticated or present")
