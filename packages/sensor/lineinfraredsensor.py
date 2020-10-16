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
        super(LineInfraRedSensor, self).__init__(position, pin)

    def _ir_sensor_event(self):
        pub.sendMessage("line_ir_sensor_event", position=self._position)
