import csv

import serial

from detection.detect import detect
from validation.validator import validate


def wakeup_arduino(ser):
    ser.write(b'9')


ser = serial.Serial('/dev/ttyACM1', 115200)


with open('trainingdata_file.csv', mode='w') as testdata_file:
    file_writer = csv.writer(testdata_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    file_writer.writerow(['Filename', 'ClassId'])

    i = 0
    sign_type = 1
    current_environment = 'a'

    while True:
        wakeup_arduino(ser)
        test_img = detect(ser)
        if validate(test_img):
            file_name = current_environment + str(i) + ".ppm"
            test_img.save("training_images/" + file_name)

            file_writer.writerow([file_name, str(sign_type)])
            i += 1
        if i % 250 == 0 and i % 1750 != 0:
            print("CHANGE SIGN")
            input()
            sign_type += 1
        if i % 1750 == 0:
            print("CHANGE ENVIRONMENT AND SIGN")
            current_environment = input()
            sign_type = 1
