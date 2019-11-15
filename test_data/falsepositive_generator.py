import csv

import serial

from detection.detect import detect
from validation.validator import validate


def wakeup_arduino(ser):
    ser.write(b'9')


ser = serial.Serial('/dev/ttyACM0', 115200)


print("How many images do you want of each sign type: ")
amt_of_each_sign = int(input())
# amt_of_each_sign = 20

print("Specify first sign type "
      "(triangle, stop etc.): ")
sign_type = str(input())

print("Give the name of the current environment: ")
current_environment = input()

print("Specify the first image number "
      "(usually 0, unless appending to existing environment): ")
i = int(input())

while True:
    wakeup_arduino(ser)
    test_img = detect(ser)

    validated, coordinates = validate(test_img)

    if validated:
        file_name = current_environment + "_" + sign_type + str(i) + ".ppm"
        test_img.save("new_false_positives/" + file_name)

        i += 1

        print("current frame: ", i)

        if i % amt_of_each_sign == 0:
            print("CHANGE SIGN")
            print("Specify first sign type "
                  "(triangle, stop etc.): ")
            sign_type = str(input())

