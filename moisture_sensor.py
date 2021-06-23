#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import send_mail as mail
from dotenv import load_dotenv, set_key
import os
from datetime import datetime
import json


f = open("config.json")
config = json.load(f)
GPIO.setmode(GPIO.BCM)

for sensor in config['sensors']:
    SENSOR_ENV_KEY='SENSOR_STATE'+sensor['name']
    ENV_PATH='/home/pi/Python/.env'
    load_dotenv(ENV_PATH)

    if os.getenv(SENSOR_ENV_KEY) == None:
        previousState=-1
    else:
        previousState= int(os.environ[SENSOR_ENV_KEY])
    GPIO.setup(sensor['channel'], GPIO.IN)
    GPIO.setup(sensor['powerPin'], GPIO.OUT)

    print("Lecture de la sonde du {} le  {} : ".format(sensor['name'], datetime.today().strftime('%Y-%m-%d-%H:%M:%S')))
    GPIO.output(sensor['powerPin'], GPIO.HIGH)
    time.sleep(0.2)
    currentState=GPIO.input(sensor['channel'])
    if currentState == previousState:
        print("Aucun changement")
    elif currentState:
        print("Il n'y a plus d'eau")
        set_key(ENV_PATH, SENSOR_ENV_KEY, str(currentState))
        mail.send_email("Il n'y a plus d'eau, il faut arroser le {}".format(sensor['name']), sensor['name'])
    else:
        print("Le {} est hydraté".format(sensor['name']))
        set_key(ENV_PATH, SENSOR_ENV_KEY, str(currentState))
        mail.send_email("Le {} est bien hydrate !".format(sensor['name']), sensor['name'])
        GPIO.output(sensor['powerPin'], GPIO.LOW)
GPIO.cleanup()
f.close()

