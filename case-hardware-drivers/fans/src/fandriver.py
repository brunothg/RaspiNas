from gpiozero import DigitalOutputDevice
from gpiozero import CPUTemperature
from gpiozero.threads import GPIOThread
import threading


class Fan(DigitalOutputDevice):
    __autoTemperature = 75.0
    __autoTemperatureTolerance = 5
    __cpuTemp = CPUTemperature()
    __speedThread = None

    def __init__(self, pin=None, active_high=True, initial_value=False, pin_factory=None):
        super().__init__(pin=pin, active_high=active_high, initial_value=initial_value, pin_factory=pin_factory)

    def __startControlSpeed(self):
         if self.__speedThread is None:
             self.__speedThread = GPIOThread(target=self.__controlSpeed)
             self.__speedThread.start()

    def __controlSpeed(self):
        addTemp = 0
        while not self.__speedThread.stopping.wait(1):
            if self.getTemperature() > (self.getAutoTemperature() + addTemp):
                self.__son()
                addTemp = -1 * self.getAutoTemperatureTolerance()
            elif self.getTemperature() < (self.getAutoTemperature() + addTemp):
                self.__soff()
                addTemp = +1 * self.getAutoTemperatureTolerance()
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

    def setAutoTemperature(self, autoTemp):
        self.__autoTemperature = autoTemp

    def getAutoTemperature(self):
        return self.__autoTemperature

    def setAutoTemperatureTolerance(self, autoTempTolerance):
        self.__autoTemperatureTolerance =  abs(autoTempTolerance)

    def getAutoTemperatureTolerance(self):
        return self.__autoTemperatureTolerance

    def close(self):
        self.__stopControlSpeed()
        self.off()
        super().off()
        super().close()
