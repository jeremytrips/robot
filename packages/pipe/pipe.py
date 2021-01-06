import settings

import serial
from serial import Serial
from packages.logger.logger import WARN, LOG, WARN_ONCE


class Pipe:

    def __init__(self):
        self.__connected = False
        try:
            self.__port = settings.SERIAL_PORT
            self.__baud_rate = 9600
            self.__serial = Serial(self.__port, baudrate=self.__baud_rate)
            self.__print_serial = settings.DEBUG_LOG
            self.__connected = True
        except serial.SerialException:
            self.__print_serial = True
            WARN(f"Serial port '{settings.SERIAL_PORT}' not found. Logging data on console.")

    def write(self, message):
        message = str(message) 
        message += settings.END_CHAR
        if self.__print_serial:
            LOG("Pipe: ", message)
        if self.__connected:
            self.__serial.write(message.encode('utf-8'))
        else:
            WARN_ONCE("/!\\    Serial port not open    /!\\")
