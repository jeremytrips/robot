import time

from packages.sensor.lineinfraredsensor import LineInfraRedSensor
from packages.sensor.ultrasonicsensor import UltraSonicSensor
from packages.pipe.pipe import Pipe
from pubsub import pub

from packages.logger.logger import LOG, WARN, WARN_ONCE
import settings


class Robot:

    def __init__(self, turn_right):
        if settings.DEBUG:
            LOG("Debug mode, using pi emulator")
        self.__turn_right = turn_right
        self.__run = False
        self.__front_distance = int(0)

        self.__front_sensor = UltraSonicSensor("front", 2, 5)
        self.__left_line_ir_sensor = LineInfraRedSensor("left", 7)

        self.__pipe = Pipe()
        pub.subscribe(listener=self._line_ir_event, topicName='line_ir_sensor_event')
        pub.subscribe(listener=self._junction_ir_event, topicName='junction_ir_sensor_event')
        pub.subscribe(listener=self._us_event, topicName='us_sensor_event')

    def run(self):
        while True:
            time.sleep(0.1)

    def _line_ir_event(self, position):
        # todo handle the reception of the message and react in consequence.
        WARN("_line_ir_event not defined yet.")

    def _junction_ir_event(self, postion):
        # todo handle the reception of the message and react in consequence.
        WARN("_junction_ir_event not defined yet.")

    def _us_event(self):
        # todo rotate of 180° the robot
        WARN_ONCE("_us_event not defined yet.")
        self.__front_distance = self.__front_sensor.distance
