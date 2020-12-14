import threading
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout

from pubsub import pub
from emulator.RPi.GPIO import GPIO
from emulator.interface.pinlayout import PinLayout
from emulator.logger.logger import LOG, WARN, ERROR
from .stateindicator import StateIndicator


class MainLayout(GridLayout):
    
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        LOG("Initiate MainLayout at", id(self))

    def set_pin(self, pin):
        # todo Add a PinLayout widget in the ScrollView
        pin_layout = PinLayout(pin=pin)
        self.add_widget(pin_layout)


class EmulatorApp(App):
    pin_layout_list = []
    main_layout = None

    def __init__(self, robot, rotation_type):
        super(EmulatorApp, self).__init__()
        pub.subscribe(self.set_pin, "add_pin_event")
        self.__robot = robot
        self.__rotation_type = rotation_type

    def on_start(self):
        LOG("Setting up Emulator")
        for layout in self.root.children:
            if type(layout) == MainLayout:
                self.main_layout = layout
        robot = self.__robot
        threading.Thread(target=robot.run).start()

    def set_pin(self, pin):
        if pin not in self.pin_layout_list:
            self.pin_layout_list.append(pin)
            self.main_layout.set_pin(pin)
        else:
            ERROR("Pin", pin.pin, "was set two times.²")


if __name__ == '__main__':
    pass
