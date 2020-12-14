 # -*- coding:utf-8 -*-
import threading

import settings
from packages.robot.robot import Robot
from packages.logger.logger import LOG

if settings.USE_EMULATOR:
    from emulator.RPi.GPIO import GPIO
else:
    import RPi.GPIO as GPIO


if __name__ == "__main__":
    # todo parse arguments
    GPIO.setmode(GPIO.BCM)
    a = Robot(True)
    try:
        a.run()
    except Exception as e:
        LOG("An unexcpeted error occurs")
        LOG(e)
    finally:
        a.kill()
        GPIO.cleanup()
