#!/usr/bin/python3

import time
import sys
import os
import getopt
import json
import systemd.daemon
import signal
import subprocess
import shlex
from gpiozero import DigitalOutputDevice

class AtxPowerService:
    __running = False

    def __init__(self, config):
        self.__config = config
        self.__atxPowerSwitch = DigitalOutputDevice(self.__config["gpio"])
        signal.signal(signal.SIGINT, self.__onSignal)
        signal.signal(signal.SIGTERM, self.__onSignal)

    def start(self):
        if self.__running:
            return

        print('Service started')

        self.__atxPowerSwitch.on()
        time.sleep(10)
        try:
            subprocess.call(shlex.split(self.__config["runAfterPowerUp"]))
        except:
            pass

        self.__running = True
        systemd.daemon.notify("READY=1")
        while self.__running:
            time.sleep(2)

    def __onSignal(self, signum, frame):
        self.stop()

    def stop(self):
        if not self.__running:
            return

        print('Service stopping ...')
        systemd.daemon.notify("STOPPING=1")
        self.__running = False

        sys.exit(os.EX_OK)


# Main Method
def main(argv):
    configFilePath = "/etc/case-hardware-driver/atx-power.json"

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
        service = AtxPowerService(config)
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