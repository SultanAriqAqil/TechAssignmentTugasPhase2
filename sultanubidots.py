import time
import requests
import math
import random

TOKEN = "BBFF-EbOfXqwIZoG6ylNinzTZaN3EUv6Bs7"  # Put your TOKEN here
DEVICE_LABEL = "raspi-4-d-manis"  # Put your device label here 
VARIABLE_LABEL_1 = "ultrasonic-sensor"  # Put your first variable label here
VARIABLE_LABEL_2 = "temperature-ruangan"
VARIABLE_LABEL_3 = "humidity"


def build_payload(variable_1,variable_2,variable_3):
    # Creates two random values for sending data
    sensor_ultrasonic = int(random.randint(0 , 200))

    sensor_suhu = int(random.randint(0, 100))

    sensor_humidity = int(random.randint(273,373))

    # Creates a random gps coordinates
    lat = random.randrange(34, 36, 1) + \
        random.randrange(1, 1000, 1) / 1000.0
    lng = random.randrange(-83, -87, -1) + \
        random.randrange(1, 1000, 1) / 1000.0
    
    payload = {variable_1: sensor_ultrasonic, variable_2: sensor_suhu, variable_3: sensor_humidity
               }

    return payload


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


def main():
    payload = build_payload(
        VARIABLE_LABEL_1,
        VARIABLE_LABEL_2,
        VARIABLE_LABEL_3
    )

    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")


if __name__ == '__main__':
    while (True):
        main()
        time.sleep(1)