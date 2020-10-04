import settings

import serial
from serial import Serial
from packages.logger.logger import WARN, LOG


class Pipe:

    def __init__(self):
        try:
            self.__port = settings.SERIAL_PORT
            self.__baud_rate = 9600
            self.__serial = Serial(self.__port, baudrate=self.__baud_rate)
            self.__print_serial = False
        except serial.SerialException:
            self.__print_serial = True
            WARN(f"Serial port '{settings.SERIAL_PORT}' not found. Logging data on console.")

    def write(self, message):
        message += settings.END_CHAR
        if self.__print_serial:
            LOG("Pipe: ", message)
        else:
            self.__serial.write(message.encode('utf-8'))
