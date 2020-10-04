from pubsub import pub

from emulator.logger.logger import LOG, WARN


class Pin:

    def __init__(self, pin_number, direction, initial=False):
        self.__pin = pin_number
        self.__direction = direction
        self.__state = initial
        self.__old_state = initial

        self.__has_event_setup = False
        self.__event_type = None
        self.__event_handler = None

    def __str__(self):
        return str(self.__pin)

    @property
    def pin(self):
        return self.__pin

    @property
    def direction(self):
        return self.__direction
    
    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        LOG(self.__state)
        self.__old_state = self.__state
        self.__state = value

        event_type = None
        if self.__old_state and not self.__state:
            event_type = 7
        elif not self.__old_state and self.__state:
            event_type = 6
        LOG("Sending 'pin_event'", "RISING" if event_type == 6 else "FALLING", "from", self.__pin)
        pub.sendMessage("pin_event", pin=self.__pin, event_type=event_type)

    @property
    def has_event_setup(self):
        return self.__has_event_setup

    @has_event_setup.setter
    def has_event_setup(self, value):
        self.__has_event_setup = value

    @property
    def event_type(self):
        return self.__event_type
    
    @event_type.setter
    def event_type(self, value):
        self.__event_type = value

    @property
    def event_handler(self):
        return self.__event_handler
    
    @event_handler.setter
    def event_handler(self, value):
        self.__event_handler = value

