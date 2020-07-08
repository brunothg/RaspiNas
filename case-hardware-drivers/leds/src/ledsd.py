#!/usr/bin/python3

import time
import sys
import os
import getopt
import json
import systemd.daemon
import signal
from gpiozero import LED

class LedsService:
    leds = {}

    def __init__(self, config):
        self.config = config
        signal.signal(signal.SIGINT, self.__onSignal)
        signal.signal(signal.SIGTERM, self.__onSignal)

    def start(self):
        print('Service started')
        systemd.daemon.notify("READY=1")
        self.__setupLeds()
        self.__setupSocket()

    def __setupLeds(self):
        for ledConfig in self.config["leds"]:
            if ledConfig["name"] in self.leds:
                continue
            led = LED(pin=ledConfig["gpio"], initial_value=ledConfig["defaultOn"])
            self.leds[ledConfig["name"]] = led

    def __setupSocket(self):
        if os.path.exists(self.config["deviceUrl"]):
                os.remove(self.config["deviceUrl"])
        while True:
            time.sleep(2)

    def __onSignal(self, signum, frame):
        self.stop()

    def stop(self):
        systemd.daemon.notify("STOPPING=1")
        
        if os.path.exists(self.config["deviceUrl"]):
                os.remove(self.config["deviceUrl"])

        for led in self.leds.values():
            led.close()

        print('Service stopped')
        sys.exit(os.EX_OK)




# Main Method
def main(argv):
    configFilePath = "/etc/case-hardware-driver/leds.json"

    try:
        opts, args = getopt.getopt(argv[1:], "hc:", ["help", "config="])
    except getopt.GetoptError:
        printHelp()
        sys.exit(os.EX_USAGE)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            printHelp()
        elif opt in ("-c", "--config"):
            configFilePath = arg
    
    if os.path.exists(configFilePath) and os.path.isfile(configFilePath):
        print('Use config file: ' + configFilePath)
        config = loadConfig(configFilePath)
        service = LedsService(config)
        service.start()
    else:
        print('Config file "' + configFilePath + '" not found')
        sys.exit(os.EX_IOERR)

def loadConfig(configFilePath):
    with open(configFilePath) as configFile:
        config = json.load(configFile)
        return config

def printHelp():
    print('Usage: ' + __file__)
    print('\t-h --help\n\t\tShow this help\n')
    print('\t-c --config\n\t\tConfig file path (optional)\n')

if __name__ == "__main__":
    main(sys.argv)