import serial
from keras.models import load_model

from detection.pixy_serial_communication.serial_reader import change_motor_speed
from classification.test.test import ModelTester
from detection.detect import detect
from validation.validator import validate


def wakeup_arduino(ser):
    ser.write(b'9')


def main_print(ser, classifier):
    print("Ready to read from serial 115200")
    while True:
        wakeup_arduino(ser)
        print("Waking up arduino...")
        detected_img = detect(ser)
        print("Object was detected")

        validated = validate(detected_img)
        print("Object was validated: ", validated)

        if validated:
            new_speed = classifier.classify_single_image(detected_img.filename)
            print("detected sign is: ", new_speed)
            change_motor_speed(ser, new_speed)


def main(ser, classifier):
    while True:
        wakeup_arduino(ser)
        detected_img = detect(ser)

        validated = validate(detected_img)
        if validated:
            new_speed = classifier.classify_single_image(detected_img.filename)
            change_motor_speed(ser, new_speed)


serial_115200 = serial.Serial('/dev/ttyACM1', 115200)
classifierModel = ModelTester(load_model("classification/models/cnn_model/cnn_model8.h5"))
main_print(serial_115200, classifierModel)
