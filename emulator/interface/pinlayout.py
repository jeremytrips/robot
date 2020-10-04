from enum import Enum

from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget

from pubsub import pub

from emulator.interface.stateindicator import StateIndicator
from emulator.logger.logger import LOG
import os

"""
    LOW = 0
    HIGH = 1

    BOARD = 2
    BCM = 3

    IN = 4
    OUT = 5

    RISING = 6
    FALLING = 7
    BOTH = 8
"""


class PinLayout(BoxLayout, Widget):
    layout_color = ListProperty([1, 1, 1, 0.3])
    _id = None
    pin_number = StringProperty("")
    direction_label = StringProperty("None")
    state = BooleanProperty(False)

    def __init__(self, pin, **kwargs):
        super(PinLayout, self).__init__(**kwargs)
        self.__pin = pin
        self.set_pin(self.__pin)

    @property
    def ID(self):
        if self._id is None:
            return self._id
        else:
            return -1

    def set_pin(self, pin):
        self.layout_color = [1, 1, 1, 0.7]
        self.__pin = pin
        self._id = self.__pin.pin
        self.pin_number = str(self._id)
        if self.__pin.direction == 4:
            self.direction_label = "Input"
        else:
            self.direction_label = "Output"
        if self.__pin.state:
            self.state = True
        else:
            self.state = False

    def _handle_toggle(self, *args):
        if args[0] == "normal":
            self.__pin.state = True
        else:
            self.__pin.state = False


if __name__ == "__main__":
    pass
