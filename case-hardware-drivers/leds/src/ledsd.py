#!/usr/bin/python3

import time
import sys
import os
import getopt
import json
import systemd.daemon
import signal
import socketserver
import ledclienthandler
import threading
from gpiozero import LED

class LedsService:
    __leds = {}

    def __init__(self, config):
        self.__config = config
        signal.signal(signal.SIGINT, self.__onSignal)
        signal.signal(signal.SIGTERM, self.__onSignal)

    def getLed(self, name: str) -> LED:
        return self.__leds[name]

    def start(self):
        print('Service started')
        systemd.daemon.notify("READY=1")
        self.__setupLeds()
        self.__setupServer()

    def __setupLeds(self):
        for ledConfig in self.__config["leds"]:
            if ledConfig["name"] in self.__leds:
                continue
            led = LED(pin=ledConfig["gpio"], initial_value=ledConfig["defaultOn"])
            self.__leds[ledConfig["name"]] = led

    def __setupServer(self):
        if hasattr(self, '__ledserver'):
            return
        if os.path.exists(self.__config["deviceUrl"]):
                os.remove(self.__config["deviceUrl"])
        self.__ledserver = socketserver.ThreadingUnixStreamServer(self.__config["deviceUrl"], ledclienthandler.LedClientHandler)
        with self.__ledserver as server:
            server.ledservice = self

            t = threading.Thread(target=server.serve_forever)
            t.setDaemon(True)
            t.start()
            t.join()

    def __onSignal(self, signum, frame):
        self.stop()

    def stop(self):
        print('Service stopping ...')
        systemd.daemon.notify("STOPPING=1")
        
        self.__tearDownServer()
        
        for led in self.__leds.values():
            led.close()

        sys.exit(os.EX_OK)

    def __tearDownServer(self):
        if not hasattr(self, '__ledserver'):
            return

        server = self.__ledserver
        del(self.__ledserver)
        server.shutdown_request()

        if os.path.exists(self.__config["deviceUrl"]):
                os.remove(self.__config["deviceUrl"])




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