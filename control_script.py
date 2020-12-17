import keyboard
from packages.logger.logger import LOG

from packages.robot.robot import Robot

a = Robot(True)


while True:  # making a loop
    if keyboard.is_pressed('q'):  # if key 'q' is pressed 
        a.control("left")
        while(keyboard.is_pressed('q')):
            pass
        a.control()
    if keyboard.is_pressed('z'):
        a.control("front")
        while(keyboard.is_pressed('z')):
            pass
        a.control()
    if keyboard.is_pressed('d'):
        a.control("right")
        while(keyboard.is_pressed('d')):
            pass
        a.control()
    if keyboard.is_pressed('s'):
        a.control("back")
        while(keyboard.is_pressed('s')):
            pass
        a.control()
    if keyboard.is_pressed('p'):
        break
