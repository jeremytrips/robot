
from emulator.logger.logger import LOG, WARN, ERROR
from emulator.pin.pin import Pin

import threading
from pubsub import pub


class _GPIO:
    LOW = 0
    HIGH = 1

    BOARD = 2
    BCM = 3

    IN = 4
    OUT = 5

    RISING = 6
    FALLING = 7
    BOTH = 8

    def __init__(self):
        self.__mode = int()
        self.__pin = dict()
        pub.subscribe(self._event_handler, "pin_event")
    
    def setmode(self, mode):
        self.__mode = mode
    
    def getmode(self):
        return self.__mode

    def setup(self, pin, direction, initial=0):
        LOG("Setting pin", pin, "as", "INPUT" if direction == 4 else "OUTPUT")
        pin = Pin(pin, direction, initial)
        pub.sendMessage("add_pin_event", pin=pin)
        if str(pin) in self.__pin.keys():
            ERROR("Pin can not be setup twice. Call cleanup before redefining please.")
        else:
            self.__pin[str(pin)] = pin

    def input(self, pin):
        try:
            if str(pin) not in self.__pin.keys():
                ERROR(f"Attempt to read a pin that has not been setup. ({pin})")
        except KeyError:
            pass
        return self.__pin[str(pin)].state
    
    def output(self, pin, value):
        if self.__pin[str(pin)].direction != _GPIO.OUT:
            ERROR(f"Attempt to write an input pin. ({pin})")
        if str(pin) not in self.__pin.keys():
            ERROR(f"Attempt to write a pin that has not been setup. ({pin})")

        self.__pin[str(pin)].state = value

    def add_event_detect(self, pin, event, callback, debouncetime=300):
        event_type = str()
        if event == 6:
            event_type = "RISING"
        elif event == 7:
            event_type = "FALLING"
        elif event == 8:
            event_type = "BOTH"
        else:
            ERROR("Got unexpected event type when adding event detect. (GOT", event, ")")
        LOG(f"Event '{event_type}' added to pin {pin}")
        pin = self.__pin[str(pin)]
        if pin.has_event_setup:
            ERROR("Pin can only have one event callback")
        pin.has_event_setup = True
        pin.event_type = event
        pin.event_handler = callback
    
    def _event_handler(self, pin, event_type):
        pin = self.__pin[str(pin)]
        if pin.event_type == event_type and pin.has_event_setup:
            pin.event_handler()

    def remove_event_detect(self, pin):
        pin = self.__pin[str(pin)]
        pin.has_event_setup = False
        pin.event_type = None
        pin.event_handler = None

    def cleanup(self):
        LOG("Cleaning up GPIO")
        self.__pin.clear()


GPIO = _GPIO()
