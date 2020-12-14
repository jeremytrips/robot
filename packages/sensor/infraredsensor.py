import settings
from packages.sensor.sensor import Sensor

from pubsub import pub
if settings.USE_EMULATOR:
    from emulator.RPi.GPIO import GPIO
else:
    import RPi.GPIO as GPIO


class InfraRedSensor(Sensor):

    def __init__(self, position, pin):
        self._position = position
        self._pin = pin
        GPIO.setup(self._pin, GPIO.IN)
        self.add_event_detect()

    def remove_event(self):
        GPIO.remove_event_detect(self._pin)

    def add_event_detect(self):
        GPIO.add_event_detect(
            self._pin,
            GPIO.FALLING,
            callback=self._ir_sensor_event
        )
    
    @property
    def state(self):
        return GPIO.input(self._pin)

    def _ir_sensor_event(self, pin):
        raise NotImplementedError()
