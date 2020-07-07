#!/usr/bin/python3

from gpiozero import DigitalOutputDevice
from time import sleep
import sys

onTime = 20
if (len(sys.argv) > 1):
    onTime = int(sys.argv[1])

print('Setup ATX')
atxPowerSupply = DigitalOutputDevice(17)

print('Power on')
atxPowerSupply.on()

sleep(onTime)

print('Power off')
atxPowerSupply.off()

print('Bye')
atxPowerSupply.close()
