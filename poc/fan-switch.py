#!/usr/bin/python3

from gpiozero import Button
from time import sleep

print('Setup FAN switch')
fanswitch1 = Button(23)
fanswitch2 = Button(24)

for i in range(100):
    sleep(1)
    
    state = (fanswitch1.is_held, fanswitch2.is_held)

    print(state)

fanswitch1.close()
fanswitch2.close()