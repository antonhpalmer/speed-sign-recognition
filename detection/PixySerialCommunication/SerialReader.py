#  Copyright (c) 2019.
#  AAU, Student project group sw504e19, 2019.
#  Use this as reference to coding conventions in Python: https://github.com/kengz/python

import serial
import re

from detection.PixySerialCommunication.PixySnapper import get_cropped_image


def get_string_from_pattern(pattern, data_string):
    info = re.search(pattern, data_string)
    if info:
        return info.group(1)
    else:
        return ""

# TODO: få lavet så den tager en serial ind i stedet.
def get_serial_data(serial_number):
    ser = serial.Serial('/dev/ttyACM0', serial_number)
    print("Ready to read serial: ", serial_number)
    # We have an error msg on the first line which we ignore.
    ser.readline()

    data = ser.readline()
    data_string = str(data)

    # We just give a regular expression equal to what we are looking for in the data string.
    x = get_string_from_pattern('x:(.+?),', data_string)
    y = get_string_from_pattern('y:(.+?),', data_string)
    w = get_string_from_pattern('w:(.+?),', data_string)
    h = get_string_from_pattern('h:(.+?),', data_string)

    print("x:", x, "y:", y, "w:", w, "h:", h)
    return get_cropped_image(int(x), int(y), int(w), int(h))
