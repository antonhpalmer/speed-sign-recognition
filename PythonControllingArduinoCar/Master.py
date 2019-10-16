#  Copyright (c) 2019.
#  AAU, Student project group sw504e19, 2019.
#  Use this as reference to coding conventions in Python: https://github.com/kengz/python

import serial


def high_speed():
    arduinoData.write(b'1')


def medium_speed():
    arduinoData.write(b'2')


def low_speed():
    arduinoData.write(b'3')


def stop_motor():
    arduinoData.write(b'4')


arduinoData = serial.Serial('com11', 115200)

x = 90

while x != 9:
    x = input()

    if x == '1':
        high_speed()
    elif x == '2':
        medium_speed()
    elif x == '3':
        low_speed()
    elif x == '4':
        stop_motor()
