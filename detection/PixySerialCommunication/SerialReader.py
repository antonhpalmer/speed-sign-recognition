#  Copyright (c) 2019.
#  AAU, Student project group sw504e19, 2019.
#  Use this as reference to coding conventions in Python: https://github.com/kengz/python

import serial
import re
from detection.PixySerialCommunication.SerialException import SerialInputException
from detection.PixySerialCommunication.PixySnapper import get_cropped_image


def get_string_from_pattern(pattern, data_string):
    info = re.search(pattern, data_string)
    if info:
        return info.group(1)
    else:
        raise SerialInputException('We did find the pattern:', pattern, ", in our data string: ", data_string)


# TODO: få lavet så den tager en serial ind i stedet.
def get_serial_data(ser):
    while True:
        data = ser.readline()
        data_string = str(data)
        try:
            # We just give a regular expression equal to what we are looking for in the data string.
            x = get_string_from_pattern('x:(.+?),', data_string)
            y = get_string_from_pattern('y:(.+?),', data_string)
            w = get_string_from_pattern('w:(.+?),', data_string)
            h = get_string_from_pattern('h:(.+?),', data_string)
        except SerialInputException as e:
            print(e)
        else:
            print("x:", x, "y:", y, "w:", w, "h:", h)
            return get_cropped_image(int(x), int(y), int(w), int(h))


ser1 = serial.Serial('COM4', 115200)
get_serial_data(ser1)
