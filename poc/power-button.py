#!/usr/bin/python3

import time
from gpiozero import Button

powerButton = Button(pin=3, bounce_time=0.01)

while True:
    powerButton.wait_for_press()
    print('Clicked')
    time.sleep(1)

powerButton.close()
