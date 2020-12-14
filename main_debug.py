import threading

import settings

from kivy.app import App
from packages.robot import robot
from emulator.RPi.GPIO import GPIO
from emulator.interface.application import EmulatorApp

if __name__ == "__main__":
    # todo parse arguments
    a = robot.Robot(True)
    app = EmulatorApp(a, True)
    try:
        app.run()
    finally:
        a.kill()
        app.stop()
        GPIO.cleanup()
