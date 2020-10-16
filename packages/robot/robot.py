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
    import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class Robot:

    def __init__(self, turn_right):
        if settings.DEBUG:
            LOG("Debug mode, using pi emulator")
        self.__turn_right = turn_right
        self.__run = False
        self.__front_distance = int(0)

        self.__front_sensor = UltraSonicSensor("front", 23, 24)
        self.__left_junction_ir_sensor = JunctionInfraRedSensor("left", 7)
        self.__left_line_ir_sensor = LineInfraRedSensor("left", 8)
        self.__right_line_ir_sensor = LineInfraRedSensor("right", 9)
        self.__right_junction_ir_sensor = JunctionInfraRedSensor("right", 10)

        self.__pipe = Pipe()
        pub.subscribe(listener=self._line_ir_event, topicName='line_ir_sensor_event')
        pub.subscribe(listener=self._junction_ir_event_handler, topicName='junction_ir_sensor_event')
        pub.subscribe(listener=self._us_event, topicName='us_sensor_event')

    def run(self):
        while True:
            time.sleep(0.1)

        self.__front_sensor.distance

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

        if position == "right" :                                        #xx1x
            if self.__right_junction_ir_sensor.state :                  #xx11
                self.__pipe.write("Tournant a droite")
            elif self.__right_junction_ir_sensor.state == False :       #xx10
                if self.__left_line_ir_sensor.state == False :          #x010
                    self.__pipe.write("Redirect a droite")
                else :                                                  #x110
                    if self.__left_junction_ir_sensor.state == False :  #0110
                        self.__pipe.write("Tout droit")
                    else :                                              #1110
                        if self.__front_sensor.distance < 15 :
                            self.__pipe.write("Tournant a gauche")
                        else : 
                            self.__pipe.write("Redirect a droite")


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
                    self.__pipe.write("Tournant a gauche")
                else : 
                    if self.__right_line_ir_sensor.state == False :     #110x
                        self.__pipe.write("Redirect a gauche")
                    else :                                              #111x
                        if self.__right_junction_ir_sensor :        #1111
                            self.__pipe.write("Tournant a droite")
                        else :                                      #1110
                            self.__pipe.write("Redirect a droite")
            else :                                                      #01xx 
                if self.__right_line_ir_sensor.state == False :         #010x
                    if self.__right_junction_ir_sensor.state :          #0101
                        self.__pipe.write("Tout droit")                 
                    else :                                              #0100    
                        self.__pipe.write("Redirect a gauche")
                else :                                                  #011x
                    if self.__right_junction_ir_sensor.state :          #0111
                        self.__pipe.write("Tournant a droite")
                    else :                                              #0110
                        self.__pipe.write("Tout droit")


        else:
            ERROR("Unexpected argument at _line_ir_event", position)
        #WARN("_line_ir_event not defined yet.")

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
                    self.__pipe.write("Tournant a droite")
                else :                                                                              #1100, 1101 et 1110
                    if self.__front_sensor.distance < 15 :
                        self.__pipe.write("Tournant a gauche")
                    else :
                        if self.__right_junction_ir_sensor.state :                  #1101
                            self.__pipe.write("Redirect a gauche")
                        else :                                                              
                            if self.__right_line_ir_sensor.state  :                 #1110
                                self.__pipe.write("Redirect a droite")
                            else :                                                  #1100
                                self.__pipe.write("Tout droit")
            else :                                                                                  #10xx
                if self.__right_line_ir_sensor.state :                                              #101x
                    if self.__right_junction_ir_sensor :                                            #1011
                        self.__pipe.write("Tournant a droite")
                    else :                                                                          #1010
                        self.__pipe.write("Redirect a gauche")
                else :                                                                              #100x
                    if self.__right_junction_ir_sensor.state :                                      #1001
                        self.__pipe.write("Tout droit")
                    else :
                        self.__pipe.write("Redirect a gauche")
        

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
                self.__pipe.write("Tournant a droite")
            else :                                                          #xx01
                if self.__left_line_ir_sensor.state :                           #x101
                    if self.__left_junction_ir_sensor.state :                       #1101
                        if self.__front_sensor.distance < 15 :
                            self.__pipe.write("Tournant a gauche")
                        else : 
                            self.__pipe.write("Redirect a gauche")
                    else :                                                          #0101
                        self.__pipe.write("Tout droit")
                else :                                                          #x001
                    if self.__left_junction_ir_sensor.state :                       #1001
                        self.__pipe.write("Tout droit")
                    else :                                                          #0001
                        self.__pipe.write("Redirect a droite")
                    
        else:
            ERROR("Unexpected argument at _line_ir_event", position)
        #self.__left_line_ir_sensor.add_event_detect()

    def _us_event(self):
        # todo rotate of 180 the robot
        self.__pipe.write("Mur en face")
        self.__front_distance = self.__front_sensor.distance
