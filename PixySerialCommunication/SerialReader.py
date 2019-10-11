#  Copyright (c) 2019.
#  AAU, Student project group sw504e19, 2019.
#  Use this as reference to coding conventions in Python: https://github.com/kengz/python

import sys
import os
from subprocess import Popen
import serial
import re
# from PixyCommunication.PixySnapper import PixySnapper

def get_string_from_pattern(pattern, data_string):
    info = re.search(pattern, data_string)
    if info:
        return info.group(1)
    else:
        return ""


def get_serial_data(serial_number):
    # snapper = PixySnapper()

    ser = serial.Serial('COM4', serial_number)
    print("Ready to read serial: ", serial_number)
    # We have an error msg on the first line which we ignore.
    ser.readline()

    while True:
        data = ser.readline()
        data_string = str(data)

        # We just give a regular expression equal to what we are looking for in the data string.
        x = get_string_from_pattern('x:(.+?),', data_string)
        y = get_string_from_pattern('y:(.+?),', data_string)
        w = get_string_from_pattern('w:(.+?),', data_string)
        h = get_string_from_pattern('h:(.+?),', data_string)

        print("x:", x, "y:", y, "w:", w, "h:", h)
        # snapper.get_cropped_image(x, y, w, h)


get_serial_data(115200)
