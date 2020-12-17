import time
from threading import Thread
import sys

from packages.sensor.lineinfraredsensor import LineInfraRedSensor
from packages.sensor.junctioninfraredsensor import JunctionInfraRedSensor
from packages.sensor.ultrasonicsensor import UltraSonicSensor
from packages.pipe.pipe import Pipe
from pubsub import pub


from packages.logger.logger import LOG, WARN, WARN_ONCE, ERROR
import settings

if settings.USE_EMULATOR:
    from emulator.RPi.GPIO import GPIO
else:
    import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

STRAIGHT = 0
ROTATE_RIGHT = 4
ROTATE_LEFT = 5
STOP = 6
CORRECT_RIGHT = 7
CORRECT_LEFT  = 8

GO_STRAIGHT_BEFORE_TURN_TIME = 0.3
TURN_FOR_180_DEGRE = 0.5

class Robot:

    def __init__(self, turn_right):
        if settings.DEBUG:
            LOG("Debug mode")
        self.__turn_right = turn_right
        self.__run = True
        self.__front_distance = int(0)

        self.__front_sensor = UltraSonicSensor("front", 23, 24)
        self.__left_junction_ir_sensor = JunctionInfraRedSensor("left", 17)
        self.__left_line_ir_sensor = LineInfraRedSensor("left", 27)
        self.__right_line_ir_sensor = LineInfraRedSensor("right", 22)
        self.__right_junction_ir_sensor = JunctionInfraRedSensor("right", 5)

        self.__pipe = Pipe()
        pub.subscribe(listener=self._line_ir_event, topicName='line_ir_sensor_event')
        pub.subscribe(listener=self._us_event, topicName='us_sensor_event')        
        time.sleep(2)
        LOG("Waiting for serial port to open")
        if settings.DEBUG:
            Thread(target=self.debug_thread).start()

    def run(self):
        """ 
        Main loop but do nothing as we use event to modify the state.
        """
        self.__pipe.write(STRAIGHT)
        while self.__run:
            time.sleep(0.1)
        self.__front_sensor.distance

    def kill(self):
        """
        Set every loop thread to flag to false
        """
        LOG("Kill main and secondary thread")
        self.__pipe.write(STOP)
        self.__run = False
        self.__front_sensor.kill()

    def remove_event_listener(self):
        pub.unsubscribe(listener=self._line_ir_event, topicName='line_ir_sensor_event')
    
    def add_event_listener(self):
        pub.subscribe(listener=self._line_ir_event, topicName='line_ir_sensor_event')

    def _line_ir_event(self, position):
        """
            Verifier si c'est possible que les deux capteurs ne soient pas ensemble sur la ligne noir.
        """
        if position == "right":
            if self.__right_junction_ir_sensor.state:
                # turn right
                self.turn_right()
            else:
                self.__pipe.write(CORRECT_RIGHT)
        elif position == "left":
            if self.__left_junction_ir_sensor.state:
                # turn left
                self.turn_left()
            else:
                self.__pipe.write(CORRECT_LEFT)
        else:
            ERROR(f"Unexcpected argument got {position}")
    
    def turn_right(self):
        self.remove_event_listener()
        self.__pipe.write(ROTATE_RIGHT)
        while self.__right_line_ir_sensor.state:
            time.sleep(0.01)
        while self.__left_line_ir_sensor.state:
            time.sleep(0.01)
        self.__pipe.write(STRAIGHT)
        self.add_event_listener()

    def turn_left(self):
        self.remove_event_listener()
        self.__pipe.write(ROTATE_LEFT)
        while self.__left_line_ir_sensor.state:
            time.sleep(0.01)
        while self.__right_line_ir_sensor.state:
            time.sleep(0.01)
        self.__pipe.write(STRAIGHT)
        self.add_event_listener()

    def _us_event(self):
        # todo rotate of 180 the robot
        self.__pipe.write("3")
        self.__front_distance = self.__front_sensor.distance
        LOG(f"Front distance: {self.__front_distance}")
    
    def debug_thread(self):
        """
        Thread used to debug the state of the robot
        """
        sensor_list = [
            self.__front_sensor,
            self.__left_junction_ir_sensor,
            self.__left_line_ir_sensor,
            self.__right_line_ir_sensor,
            self.__right_junction_ir_sensor
        ]
        while (self.__run):
            for elem in sensor_list:
                sys.stdout.write(f"\033[K {elem.get_state()}")
            for i in range(len(sensor_list)):
                sys.stdout.write("\033[F")
            time.sleep(0.2)
            