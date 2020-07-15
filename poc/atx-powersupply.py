#!/usr/bin/python3

from gpiozero import DigitalOutputDevice
from time import sleep
import sys

on = True
if (len(sys.argv) > 1):
    on = bool(sys.argv[1])

print('Setup ATX')
atxPowerSupply = DigitalOutputDevice(17)

if on:
    print('Power on')
    atxPowerSupply.on()
else:
    print('Power off')
    atxPowerSupply.off()

while True:
    sleep(2)
