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
from gpiozero import Button

class PowerButtonService:
    __powerbutton = None
    __running = False

    def __init__(self, config):
        self.__config = config
        signal.signal(signal.SIGINT, self.__onSignal)
        signal.signal(signal.SIGTERM, self.__onSignal)

    def start(self):
        if self.__running:
            return
        print('Service started')
        self.__setPowerLed(1)
        time.sleep(1)
        self.__setPowerLed(0)

        self.__running = True
        systemd.daemon.notify("READY=1")
        self.__setupPowerButton()
        self.__listen()

    def __setupPowerButton(self):
        powerbuttonConfig = self.__config["powerbutton"]
        self.__powerbutton = Button(pin=powerbuttonConfig["gpio"])

    def __listen(self):
        while self.__running:
            time.sleep(1)
            if self.__powerbutton.value == 1:
                print("Begin shutdown sequence")
                
                self.__setPowerLed(0)
                for i in range(0, 4):
                    time.sleep(0.5)
                    self.__setPowerLed(1)
                    time.sleep(0.5)
                    self.__setPowerLed(0)

                self.__setPowerLed(1)
                beginTime = time.time()
                self.__powerbutton.wait_for_press(2)
                reacTime = time.time() - beginTime
                if reacTime > 2:
                    print("Too slow")
                    self.__setPowerLed(0)
                    continue
                
                self.__setPowerLed(0)
                time.sleep(0.3)
                self.__setPowerLed(1)
                time.sleep(0.3)
                self.__setPowerLed(0)
                print("Bye")
                subprocess.check_call(shlex.split(self.__config["shutdownCmd"]))

    def __setPowerLed(self, ledState, wait=1):
        stateValue = 0
        if ledState:
            stateValue = 1

        try:
            print("Setting led value")
            ledProcess = subprocess.Popen(["nc", "-U", "/dev/case-hardware-leds"], stdin=subprocess.PIPE)
            with ledProcess.stdin as ledStdin:
                cmd = "set-state:" + self.__config["powerled"] + ":" + str(stateValue) + "\n"
                print(cmd)
                ledStdin.write(cmd.encode("utf-8"))
            result = ledProcess.wait(wait)
            if result != 0:
                print("Error setting led value")
        except Exception as e:
            print(e)

    def __onSignal(self, signum, frame):
        self.stop()

    def stop(self):
        if not self.__running:
            return
        print('Service stopping ...')
        systemd.daemon.notify("STOPPING=1")
        
        self.__setPowerLed(False)
        self.__powerbutton.close()

        sys.exit(os.EX_OK)

# Main Method
def main(argv):
    configFilePath = "/etc/case-hardware-driver/power-button.json"

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
        service = PowerButtonService(config)
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