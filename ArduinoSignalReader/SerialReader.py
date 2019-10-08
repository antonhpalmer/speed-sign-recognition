import sys
import os
from subprocess import Popen
import serial
import re


def get_string(pattern, data_string):
    info = re.search(pattern, data_string)
    if info:
        return info.group(1)
    else:
        return ""


def get_serial_data(serial_number):
    ser = serial.Serial('COM4', serial_number)

    while True:
        data = ser.readline()
        data_string = str(data)

        # We just give a regular expression equal to what we are looking for in the data string.
        x = get_string('x:(.+?),', data_string)
        y = get_string('y:(.+?),', data_string)
        w = get_string('w:(.+?),', data_string)
        h = get_string('h:(.+?),', data_string)
        print("x:", x, "y:", y, "w:", w, "h:", h)


get_serial_data(115200)
