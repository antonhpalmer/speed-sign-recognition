import sys
import os
from subprocess import Popen
import serial
import re


def get_string_from_pattern(pattern, data_string):
    info = re.search(pattern, data_string)
    if info:
        return info.group(1)
    else:
        return ""


def get_serial_data(serial_number):
    ser = serial.Serial('COM4', serial_number)

    # We have an error msg on the first line which we ignore.
    ser.readline()

    while True:
        data = ser.readline()
        data_string = str(data)

        x = get_string_from_pattern('x:(.+?),', data_string)
        y = get_string_from_pattern('y:(.+?),', data_string)
        w = get_string_from_pattern('w:(.+?),', data_string)
        h = get_string_from_pattern('h:(.+?),', data_string)

        # We just give a regular expression equal to what we are looking for in the data string.
        print("x:", x, "y:", y, "w:", w, "h:", h)


get_serial_data(115200)
