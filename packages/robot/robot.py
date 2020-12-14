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
        pub.subscribe(listener=self._junction_ir_event_handler, topicName='junction_ir_sensor_event')
        pub.subscribe(listener=self._us_event, topicName='us_sensor_event')
        if settings.DEBUG:
            Thread(target=self.debug_thread).start()

    def run(self):
        """ 
        Main loop but do nothing as we use event to modify the state.
        """
        while self.__run:
            time.sleep(0.1)
        self.__front_sensor.distance

    def kill(self):
        """
        Set every loop thread to flag to false
        """
        LOG("Kill main and secondary thread")
        self.__run = False
        self.__front_sensor.kill()

    def _line_ir_event(self, position):
        # todo handle the reception of the message and react in consequence.
        #Si "right" == True, alors xx1x et donc :
        #0010 --- redirect vers la droite (1,0.8)
        #0011 --- tournant a droite
        #0111 --- tournant a droite et gauche mais incline a gauche (donc tournant a droite)
        #1011 --- chelou, devrait pas arriver, mais -- tournant a droite
        #1111 --- carrefour -- tournant a droite
        #0110 --- on espere que ca arrive pas -- tout droit
        #1110 --- chelou mais tournant a gauche si pas US
        #1010 --- chelou mais redirect vers la droite
        pub.unsubscribe(listener=self._junction_ir_event, topicName='line_ir_sensor_event')


        if position == "right" :                                        #xx1x
            if self.__right_junction_ir_sensor.state :                  #xx11
                self.__pipe.write("2")
            elif self.__right_junction_ir_sensor.state == False :       #xx10
                if self.__left_line_ir_sensor.state == False :          #x010
                    self.__pipe.write("4")
                else :                                                  #x110
                    if self.__left_junction_ir_sensor.state == False :  #0110
                        self.__pipe.write("0")
                    else :                                              #1110
                        if self.__front_sensor.distance < 15 :
                            self.__pipe.write("1")
                        else : 
                            self.__pipe.write("4")


        #Si "left" == True, alors x1xx et donc :
        #1100 --- Tournant a gauche -- depend du US
        #1101 --- Chelou, devrait pas arriver -- Tournant a gauche -- depend du US
        #1111 --- Carrefour, tournant a droite
        #1110 --- Tournant a gauche mais incline a droite, donc depend de US et redirection ou tournant
        #0100 --- Redirection vers la gauche
        #0110 --- on espere que ca arrive pas -- tout droit
        #0101 --- chelou mais tout droit
        #0111 --- chelou mais tournant a droite en fait

        elif position == "left" :                                       #x1xx
            if self.__left_junction_ir_sensor.state :                   #11xx
                if self.__front_sensor.distance < 15 :
                    self.__pipe.write("1")
                else : 
                    if self.__right_line_ir_sensor.state == False :     #110x
                        self.__pipe.write("5")
                    else :                                              #111x
                        if self.__right_junction_ir_sensor :        #1111
                            self.__pipe.write("2")
                        else :                                      #1110
                            self.__pipe.write("4")
            else :                                                      #01xx 
                if self.__right_line_ir_sensor.state == False :         #010x
                    if self.__right_junction_ir_sensor.state :          #0101
                        self.__pipe.write("0")                 
                    else :                                              #0100    
                        self.__pipe.write("5")
                else :                                                  #011x
                    if self.__right_junction_ir_sensor.state :          #0111
                        self.__pipe.write("2")
                    else :                                              #0110
                        self.__pipe.write("0")


        else:
            ERROR("Unexpected argument at _line_ir_event", position)
        pub.subscribe(listener=self._junction_ir_event, topicName='line_ir_sensor_event')

    #Si left == true, alors : 1xxx
    #1000 --- chelou, mais redirection vers la gauche (car ca implique qu'il y a un tournant a gauche percu avant le capteur central gauche, donc incline vers la droite)
    #1001 --- zero sens, go tout droit
    #1010 --- chelou, mais redirection vers la gauche
    #1011 --- chelou, devrait pas arriver, mais -- tournant a droite
    #1100 --- Tournant a gauche -- depend du US
    #1101 --- Chelou, devrait pas arriver -- Tournant a gauche -- depend du US
    #1110 --- Tournant a gauche mais incline a droite, donc depend de US et redirection ou tournant
    #1111 --- Carrefour, tournant a droite

    def _junction_ir_event_handler(self, position):
        # todo handle the reception of the message and react in consequence. Rotate 90 
        #self.__left_line_ir_sensor.remove_event()
        #WARN("_junction_ir_event not defined yet.")
        if position == "left" :                                                                     #1xxx
            if self.__left_line_ir_sensor.state :                                                   #11xx
                if self.__right_line_ir_sensor.state and self.__right_junction_ir_sensor.state :    #1111
                    self.__pipe.write("2")
                else :                                                                              #1100, 1101 et 1110
                    if self.__front_sensor.distance < 15 :
                        self.__pipe.write("1")
                    else :
                        if self.__right_junction_ir_sensor.state :                  #1101
                            self.__pipe.write("5")
                        else :                                                              
                            if self.__right_line_ir_sensor.state  :                 #1110
                                self.__pipe.write("4")
                            else :                                                  #1100
                                self.__pipe.write("0")
            else :                                                                                  #10xx
                if self.__right_line_ir_sensor.state :                                              #101x
                    if self.__right_junction_ir_sensor :                                            #1011
                        self.__pipe.write("2")
                    else :                                                                          #1010
                        self.__pipe.write("5")
                else :                                                                              #100x
                    if self.__right_junction_ir_sensor.state :                                      #1001
                        self.__pipe.write("0")
                    else :
                        self.__pipe.write("5")
        

        #si right == True, alors xxx1 :
        #0001 --- chelou, mais redirect droit 
        #0011 --- tournant droit
        #0111 --- tournant droit
        #1111 --- carrefour -- tournant droit
        #0101 --- tout droit (chelou)
        #1001 --- zero sens go tout droit
        #1011 --- chelou mais tournant droit
        #1101 --- chelou mais tournant gauche (selon US)

        elif position == "right" :                                    #xxx1
            if self.__right_line_ir_sensor.state :                          #xx11
                self.__pipe.write("2")
            else :                                                          #xx01
                if self.__left_line_ir_sensor.state :                           #x101
                    if self.__left_junction_ir_sensor.state :                       #1101
                        if self.__front_sensor.distance < 15 :
                            self.__pipe.write("1")
                        else : 
                            self.__pipe.write("5")
                    else :                                                          #0101
                        self.__pipe.write("0")
                else :                                                          #x001
                    if self.__left_junction_ir_sensor.state :                       #1001
                        self.__pipe.write("0")
                    else :                                                          #0001
                        self.__pipe.write("4")
                    
        else:
            ERROR("Unexpected argument at _line_ir_event", position)
        #self.__left_line_ir_sensor.add_event_detect()
        pub.subscribe(listener=self._junction_ir_event, topicName='junction_ir_sensor_event')

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
            