#!/usr/bin/python3

import time
import sys
import os
import getopt
import json
import systemd.daemon
import signal
import socketserver
import fanclienthandler
import threading
import fandriver

class FansService:
    __fans = {}

    def __init__(self, config):
        self.__config = config
        signal.signal(signal.SIGINT, self.__onSignal)
        signal.signal(signal.SIGTERM, self.__onSignal)

    def getFan(self, name: str) -> fandriver.Fan:
        return self.__fans[name]

    def start(self):
        print('Service started')
        systemd.daemon.notify("READY=1")
        self.__setupFans()
        self.__setupServer()

    def __setupFans(self):
        for fanConfig in self.__config["fans"]:
            if fanConfig["name"] in self.__fans:
                continue
            fan = fandriver.Fan(pin=fanConfig["gpio"])
            fan.setAutoTemperature(fanConfig["autoTemperature"])
            fan.setAutoTemperatureTolerance(fanConfig["autoTemperatureTolerance"])
            if fanConfig["defaultMode"] < 0:
                fan.auto()
            elif fanConfig["defaultMode"] == 0:
                fan.off()
            else:
                fan.on()

            self.__fans[fanConfig["name"]] = fan

    def __setupServer(self):
        if hasattr(self, '__fanserver'):
            return
        if os.path.exists(self.__config["deviceUrl"]):
                os.remove(self.__config["deviceUrl"])
        self.__fanserver = socketserver.ThreadingUnixStreamServer(self.__config["deviceUrl"], fanclienthandler.FanClientHandler)
        with self.__fanserver as server:
            server.fanservice = self

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
        
        for fan in self.__fans.values():
            fan.close()

        sys.exit(os.EX_OK)

    def __tearDownServer(self):
        if not hasattr(self, '__fanserver'):
            return

        server = self.__fanserver
        del(self.__fanserver)
        server.shutdown_request()

        if os.path.exists(self.__config["deviceUrl"]):
                os.remove(self.__config["deviceUrl"])




# Main Method
def main(argv):
    configFilePath = "/etc/case-hardware-driver/fans.json"

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
        service = FansService(config)
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