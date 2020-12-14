from .infraredsensor import InfraRedSensor
import pubsub.pub as pub

from ..logger.logger import LOG

import settings

if settings.DEBUG:
    from emulator.RPi.GPIO import GPIO
else:
    import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class LineInfraRedSensor(InfraRedSensor):

    def __init__(self, position, pin):
        self.__type = "Line"
        super(LineInfraRedSensor, self).__init__(position, pin)

    def _ir_sensor_event(self, pin):
        pub.sendMessage("line_ir_sensor_event", position=self._position)

    def get_state(self):
        return f"\033[92mir sensor {self._position} {self.__type}\033[0m\t\t {self.state}"
