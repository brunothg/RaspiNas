#!/usr/bin/python3

from gpiozero import Button

powerButton = Button(3)

powerButton.wait_for_press()
print('Clicked')

powerButton.close()
