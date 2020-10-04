import time

from packages.sensor.lineinfraredsensor import LineInfraRedSensor
from packages.sensor.junctioninfraredsensor import JunctionInfraRedSensor
from packages.sensor.ultrasonicsensor import UltraSonicSensor
from packages.pipe.pipe import Pipe
from pubsub import pub


from packages.logger.logger import LOG, WARN, WARN_ONCE, ERROR
import settings

if settings.DEBUG:
    from emulator.RPi.GPIO import GPIO
else:
    from RPi.GPIO import GPIO


class Robot:

    def __init__(self, turn_right):
        if settings.DEBUG:
            LOG("Debug mode, using pi emulator")
        self.__turn_right = turn_right
        self.__run = False
        self.__front_distance = int(0)

        self.__front_sensor = UltraSonicSensor("front", 2, 5)
        self.__left_line_ir_sensor = LineInfraRedSensor("left", 8)
        self.__right_line_ir_sensor = LineInfraRedSensor("right", 9)
        self.__left_junction_ir_sensor = JunctionInfraRedSensor("left", 7)
        self.__right_junction_ir_sensor = JunctionInfraRedSensor("right", 10)

        self.__pipe = Pipe()
        pub.subscribe(listener=self._line_ir_event, topicName='line_ir_sensor_event')
        pub.subscribe(listener=self._junction_ir_event, topicName='junction_ir_sensor_event')
        pub.subscribe(listener=self._us_event, topicName='us_sensor_event')

    def run(self):
        while True:
            time.sleep(0.1)



    def _line_ir_event(self, position):
        # todo handle the reception of the message and react in consequence.
        #Si "right" == True, alors xx1x et donc :
        #0010 --- redirect vers la droite (1,0.8)
        #0011 --- tournant a droite
        #0111 --- tournant a droite et gauche mais incliné a gauche (donc tournant a droite)
        #1011 --- chelou, devrait pas arriver, mais -- tournant a droite
        #1111 --- carrefour -- tournant a droite
        #0110 --- on espère que ça arrive pas -- tout droit
        #1110 --- chelou mais tournant a gauche si pas US
        #1010 --- chelou mais redirect vers la droite

        if position == "right" :                                        #xx1x
            if self.__right_junction_ir_sensor.state :                  #xx11
                self.__pipe.write("Tournant a droite")
            elif self.__right_junction_ir_sensor.state == False :       #xx10
                if self.__left_line_ir_sensor.state == False :          #x010
                    self.__pipe.write("Redirect vers la droite")
                else :                                                  #x110
                    if self.__left_junction_ir_sensor.state == False :  #0110
                        self.__pipe.write("Tout droit")
                    else :                                              #1110
                        self.__pipe.write("Tournant a gauche")
            else :
                ERROR("Unexpected argument at _line_ir_event", position)


        #Si "left" == True, alors x1xx et donc :
        #1100 --- Tournant a gauche -- depend du US
        #1101 --- Chelou, devrait pas arriver -- Tournant a gauche -- depend du US
        #1111 --- Carrefour, tournant a droite
        #1110 --- Tournant a gauche mais incliné a droite, donc dépend de US et redirection ou tournant
        #0100 --- Redirection vers la gauche
        #0110 --- on espère que ça arrive pas -- tout droit
        #0101 --- chelou mais redirect a gauche
        #0111 --- chelou mais tournant a droite en fait

        elif position == "left" :                                       #x1xx
            if self.__left_junction_ir_sensor.state :                   #11xx
                self.__pipe.write("Tournant a gauche")
            else :                                                      #01xx 
                if self.__right_line_ir_sensor.state == False :         #010x
                    self.__pipe.write("Redirect a gauche")
                else :                                                  #011x
                    if self.__right_junction_ir_sensor.state :          #0111
                        self.__pipe.write("Tournant a droite")
                    else :                                              #0110
                        self.__pipe.write("Tout droit")




        else:
            ERROR("Unexpected argument at _line_ir_event", position)
        WARN("_line_ir_event not defined yet.")


    def _junction_ir_event(self, position):
        # todo handle the reception of the message and react in consequence. Rotate 90° 
        self.__left_line_ir_sensor.remove_event()
        WARN("_junction_ir_event not defined yet.")

        self.__left_line_ir_sensor.add_event_detect()

    def _us_event(self):
        # todo rotate of 180° the robot
        WARN_ONCE("_us_event not defined yet.")
        self.__front_distance = self.__front_sensor.distance
