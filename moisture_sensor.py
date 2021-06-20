#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import send_mail as mail
from dotenv import load_dotenv, set_key
import os

SENSOR_ENV_KEY='SENSOR_STATE'
ENV_PATH='/home/pi/Python/.env'
load_dotenv(ENV_PATH)
channel=17

if os.getenv(SENSOR_ENV_KEY) == None:
    previousState=-1
else:
    previousState= int(os.environ[SENSOR_ENV_KEY])
    print(previousState)
input=4
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)
GPIO.setup(input, GPIO.OUT)

print("Lecture de la sonde à : "+ time.strftime("%H:%M:%S", time.localtime()))
GPIO.output(input, GPIO.HIGH)
time.sleep(1)
currentState=GPIO.input(channel)
if currentState == previousState:
    print("Aucun changement")
elif currentState:
    print("Il n'y a plus d'eau")
    set_key(ENV_PATH, SENSOR_ENV_KEY, str(currentState))
    mail.send_email("Il n'y a plus d'eau, il faut arroser le bonsai")
else:
    print("Le bonsai est hydraté")
    set_key(ENV_PATH, SENSOR_ENV_KEY, str(currentState))
    mail.send_email("Le bonsai est bien hydrate !")
GPIO.output(input, GPIO.LOW)
GPIO.cleanup()

