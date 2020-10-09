import threading

import settings

from packages.robot import robot

if __name__ == "__main__":
    # todo parse arguments
    
    try:
        a = Robot()
        a.run()
    finally:
        GPIO.cleanup()
