from gpiozero import DigitalOutputDevice
from gpiozero import CPUTemperature
from gpiozero.threads import GPIOThread
import threading
import subprocess
import re


class Fan(DigitalOutputDevice):
    __autoTemperature = 75.0
    __autoCooldownTemperature = 65
    __cpuTemp = CPUTemperature()
    __speedThread = None
    __smartEnabled = True
    __smartTolerance = 10
    __smartThreshold = 0
    __smartMaxTemp = 50
    __smartCooldownTemp = 40
    __smartUpdateCycle = 10

    def __init__(self, pin=None, active_high=True, initial_value=False, pin_factory=None):
        super().__init__(pin=pin, active_high=active_high, initial_value=initial_value, pin_factory=pin_factory)

    def __startControlSpeed(self):
         if self.__speedThread is None:
             self.__speedThread = GPIOThread(target=self.__controlSpeed)
             self.__speedThread.start()

    def __controlSpeed(self):
        tempState = False
        smartState = False
        smartTempState = False

        smartCounter = 0
        smartValue = (self.getSMARTTemperatureValue() - self.getSMARTTreshold())
        smartTemp = self.getSMARTTemperatureCelsius()
        while not self.__speedThread.stopping.wait(1):

            if self.getTemperature() >= self.getAutoTemperature():
                tempState = True
            elif self.getTemperature() <= self.getAutoCooldownTemperature():
                tempState = False

            if smartValue <= 0:
                smartState = True
            elif smartValue >= self.getSMARTTolerance():
                smartState = False

            if smartTemp >= self.getSMARTMaxTemperature():
                smartTempState = True
            elif smartTemp <= self.getSMARTCooldownTemperature():
                smartTempState = False

            if smartCounter > self.getSMARTUpdateCycleCount():
                smartCounter = 0
                smartValue = (self.getSMARTTemperatureValue()  - self.getSMARTTreshold())
                smartTemp = self.getSMARTTemperatureCelsius()
            else:
                smartCounter = smartCounter + 1

            if tempState or smartState or smartTempState:
                self.__son()
            else:
                self.__soff()
        self.__soff()

    def __stopControlSpeed(self):
        if self.__speedThread is not None:
            if self.__speedThread.is_alive():
                self.__speedThread.stop()
            self.__speedThread = None

    def on(self):
        self.__stopControlSpeed()
        self.__son()

    def __son(self):
        super().on()

    def off(self):
        self.__stopControlSpeed()
        self.__soff()

    def __soff(self):
        super().off()

    def auto(self):
        self.__startControlSpeed()

    def getTemperature(self):
        return self.__cpuTemp.temperature

    def __getHDDs(self):
        try:
            response = subprocess.check_output(["smartctl", "--scan"])
            
            disks = list()
            for diskline in response.splitlines():
                diskline = diskline.strip()
                disklineparts = diskline.decode('utf-8').split(' ')
                disks.append(disklineparts[0])

            return disks
        except Exception as e:
            # print(e)
            pass
        return []

    def getSMARTTemperatureValue(self):
        worst = 255

        if self.isSmartEnabled():
            disks = self.__getHDDs()
            for disk in disks:
                try:
                    response = subprocess.check_output(["smartctl", "-A", "/dev/" + disk]).decode('utf-8')
                    tempLines = list(filter(lambda x: x.startswith('194'), response.splitlines()))
                    for tempLine in tempLines:
                        tempLineParts = re.split(r"\s+", tempLine)
                        value = float(tempLineParts[3])
                        threshold = float(tempLineParts[5])
                        dif = (value - threshold)
                        worst = min(dif, worst)
                except subprocess.CalledProcessError as e:
                    # print(e)
                    pass
        
        return worst

    def getSMARTTemperatureCelsius(self):
        worst = 0

        if self.isSmartEnabled():
            disks = self.__getHDDs()
            for disk in disks:
                try:
                    response = subprocess.check_output(["smartctl", "-A", "/dev/" + disk]).decode('utf-8')
                    tempLines = list(filter(lambda x: x.startswith('194'), response.splitlines()))
                    for tempLine in tempLines:
                        tempLineParts = re.split(r"\s+", tempLine)
                        value = float(tempLineParts[9])
                        worst = max(value, worst)
                except subprocess.CalledProcessError as e:
                    # print(e)
                    pass
        
        return worst

    def setSMARTTolerance(self, tolerance):
        self.__smartTolerance = abs(tolerance)

    def getSMARTTolerance(self):
        return self.__smartTolerance

    def setSMARTTreshold(self, treshold):
        self.__smartThreshold = abs(treshold)

    def getSMARTTreshold(self):
        return self.__smartThreshold

    def setAutoTemperature(self, autoTemp):
        self.__autoTemperature = autoTemp

    def getAutoTemperature(self):
        return self.__autoTemperature

    def setAutoCooldownTemperature(self, autoCooldownTolerance):
        self.__autoCooldownTemperature =  abs(autoCooldownTolerance)

    def getAutoCooldownTemperature(self):
        return self.__autoCooldownTemperature

    def setSmartEnabled(self, enabled):
        self.__smartEnabled = enabled

    def isSmartEnabled(self):
        return self.__smartEnabled

    def setSMARTMaxTemperature(self, maxTemperature):
        self.__smartMaxTemp = abs(maxTemperature)

    def getSMARTMaxTemperature(self):
        return self.__smartMaxTemp

    def setSMARTCooldownTemperature(self, cooldownTemperature):
        self.__smartCooldownTemp = abs(cooldownTemperature)

    def getSMARTCooldownTemperature(self):
        return self.__smartCooldownTemp

    def setSMARTUpdateCycleCount(self, cycleCount):
        self.__smartUpdateCycle = cycleCount

    def getSMARTUpdateCycleCount(self):
        return self.__smartUpdateCycle

    def close(self):
        self.__stopControlSpeed()
        self.off()
        super().off()
        super().close()
