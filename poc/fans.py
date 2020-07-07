#!/usr/bin/python3

from gpiozero import DigitalOutputDevice
from time import sleep
import sys

onTime = 10
if (len(sys.argv) > 1):
    onTime = int(sys.argv[1])

print('Setup FANs')
fans = DigitalOutputDevice(26)

print('Power on')
fans.on()

sleep(onTime)

print('Power off')
fans.off()

print('Bye')
fans.close()
