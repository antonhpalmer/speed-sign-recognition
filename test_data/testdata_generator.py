import csv

import serial

from detection.detect import detect
from validation.validator import validate


def wakeup_arduino(ser):
    ser.write(b'9')


ser = serial.Serial('/dev/ttyACM0', 115200)

with open('new_testdata_file.csv', mode='a+') as csv_file:
    file_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # print("How many images do you want of each sign type: ")
    # amt_of_each_sign = int(input())
    amt_of_each_sign = 20

    print("Specify first sign type "
          "(30, 50, 60, 70, 80, 90, 100, 110, 120): ")
    sign_type = int(input())

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
            file_name = current_environment + str(i) + ".ppm"
            test_img.save("new_test_images/" + file_name)

            file_writer.writerow([file_name, str(sign_type)])
            i += 1

            print("current frame: ", i)

            if i % amt_of_each_sign == 0:
                print("CHANGE SIGN")
                print("Specify next sign type "
                      "(30, 50, 60, 70, 80, 90, 100, 110, 120): ")
                sign_type = int(input())
