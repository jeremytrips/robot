import threading

import settings

from kivy.app import App
from packages.robot import robot
from emulator.RPi.GPIO import GPIO
from emulator.interface.application import EmulatorApp

if __name__ == "__main__":
    # todo parse arguments
    app = EmulatorApp(robot.Robot, True)
    try:
        app.run()
    finally:
        app.stop()
        GPIO.cleanup()
