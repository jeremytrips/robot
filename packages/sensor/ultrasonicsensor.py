import settings
from threading import Thread
import time

from pubsub import pub
if settings.DEBUG:
    from emulator.RPi.GPIO import GPIO
    import random
else:
    import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class UltraSonicSensor:

    def __init__(self, position, gpio_trigger, gpio_echo):
        self.__position = position
        self.__front_distance = int(0)
        self.__gpio_trigger = gpio_trigger
        self.__gpio_echo = gpio_echo
        self.__distance = int(0)

        GPIO.setup(gpio_trigger, GPIO.OUT)
        GPIO.setup(gpio_echo, GPIO.IN)
        GPIO.output(gpio_trigger, GPIO.LOW)
        Thread(target=self.measure).start()
    
    def measure(self):
        while True:
            self._get_average()
            if self.__distance < 5 :
                pub.sendMessage("us_sensor_event")
            time.sleep(0.2)

    def _get_distance(self):
        if settings.DEBUG:
            return random.randint(settings.DISTANCE_LOW, settings.DISTANCE_HIGH)
        GPIO.output(self.__gpio_trigger, True)
        time.sleep(0.00001)
        GPIO.output(self.__gpio_trigger, False)
        start = time.time()

        """Les deux boucles hyper bizarre ici ont un sens, en fait quand on envoi le signal, input est HIGH
        Donc dès que le signal part le start time se fixe car on sort de la boucle 
        Puis dès que le signal revient, l'input devient LOW, et donc le stop time se fixe dès que le rebound est 
        detecte par ECHO"""

        while GPIO.input(self.__gpio_echo) == 0:
            start = time.time()

        while GPIO.input(self.__gpio_echo) == 1:
            stop = time.time()

        # Calculate pulse length
        elapsed = stop-start

        # Distance pulse travelled in that time is time
        # multiplied by the speed of sound (cm/s)
        # That was the distance there and back so halve the value
        distance = elapsed * 34000 / 2
        return distance

    def _get_average(self):
        increment = 0
        listePourMoyenne = []
        while increment < 7:
            increment += 1
            distanceMesuree = self._get_distance()
            listePourMoyenne.append(distanceMesuree)
        self.__distance = sum(sorted(listePourMoyenne)[2:-2])/(len(listePourMoyenne)-4)
        
    #petite note ici, List.sort() m'a deja renvoye None, sorted(List) jamais

    def _us_sensor_event(self):
        pub.sendMessage("us_sensor_event")

    @property
    def distance(self):
        return self.__distance