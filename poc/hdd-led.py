#!/usr/bin/python3

from gpiozero import DigitalOutputDevice
from time import sleep

print('Setup LED')
hddLed = DigitalOutputDevice(19)

print('Power on')
hddLed.on()

sleep(5)

print('Power off')
hddLed.off()

print('Bye')
hddLed.close()
