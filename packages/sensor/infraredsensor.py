import settings

from pubsub import pub
if settings.DEBUG:
    from emulator.RPi.GPIO import GPIO
else:
    from RPi.GPIO import GPIO


class InfraRedSensor:

    def __init__(self, position, pin):
        self._position = position
        self._pin = pin
        GPIO.setup(self._pin, GPIO.IN)
        GPIO.add_event_detect(
            self._pin,
            GPIO.RISING,
            callback=self._ir_sensor_event,
            debouncetime=300
        )

    def _ir_sensor_event(self):
        raise NotImplementedError()
