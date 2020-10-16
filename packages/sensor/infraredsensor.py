import settings

from pubsub import pub
if settings.DEBUG:
    from emulator.RPi.GPIO import GPIO
else:
    import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class InfraRedSensor:

    def __init__(self, position, pin):
        self._position = position
        self._pin = pin
        self._state = False
        GPIO.setup(self._pin, GPIO.IN)
        self.add_event_detect()

    def remove_event(self):
        GPIO.remove_event_detect(self._pin)

    def add_event_detect(self):
        GPIO.add_event_detect(
            self._pin,
            GPIO.RISING,
            callback=self._ir_sensor_event,
        )
    
    @property
    def state(self):
        return GPIO.input(self._pin)

    def _ir_sensor_event(self):
        raise NotImplementedError()
