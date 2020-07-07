#!/usr/bin/python3

from gpiozero import DigitalOutputDevice
from time import sleep
import sys

onTime = 5
if (len(sys.argv) > 1):
    onTime = int(sys.argv[1])

print('Setup LED')
powerLed = DigitalOutputDevice(13)

print('Power on')
powerLed.on()

sleep(onTime)

print('Power off')
powerLed.off()

print('Bye')
powerLed.close()
