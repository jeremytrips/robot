from kivy.core.image import Image
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.togglebutton import ToggleButton

from emulator.logger.logger import LOG


class StateIndicator(ToggleButton):
    background_normal = StringProperty("emulator/assets/HIGH.png")
    background_down = StringProperty("emulator/assets/LOW.png")
    
    def __init__(self, **kwargs):
        super(StateIndicator, self).__init__(**kwargs)
