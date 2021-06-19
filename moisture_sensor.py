#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import send_mail as mail

channel=17
previousState=-1
input=4
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)
GPIO.setup(input, GPIO.OUT)


while True:
    print("Lecture de la sonde à : "+ time.strftime("%H:%M:%S", time.localtime()))
    GPIO.output(input, GPIO.HIGH)
    if GPIO.input(channel) == previousState:
        print("Aucun changement")
    elif GPIO.input(channel):
        print("Il n'y a plus d'eau")
        mail.send_email("Il n'y a plus d'eau, il faut arroser le bonsai")
    else:
        print("Le bonsai est hydraté")
        mail.send_email("Le bonsai est bien hydrate !")
    previousState = GPIO.input(channel)
    GPIO.output(input, GPIO.LOW)
    time.sleep(3600)

