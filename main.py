import serial
from keras.models import load_model
from box_finder.newboxfinder import crop_image

from detection.pixy_serial_communication.serial_reader import change_motor_speed
from classification.test.test import ModelTester
from detection.detect import detect
from validation.validator import validate
from classification.definitions import ID_TO_SIGN_SWITCHER


def wakeup_arduino(ser):
    ser.write(b'9')


def main_print(ser, classifier):
    print("Ready to read from serial 115200")
    while True:
        wakeup_arduino(ser)
        print("Waking up arduino...")
        detected_img = detect(ser)
        print("Object was detected")

        validated, coordinates = validate(detected_img)
        print("Object was validated: ", validated)

        if validated:
            path = "C:/Users/frede/PycharmProjects/speed-sign-recognition/cropped.ppm"
            img = crop_image(detected_img, coordinates)
            img.save(path)
            new_speed = classifier.classify_single_image(path)
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


serial_115200 = serial.Serial('/dev/ttyACM0', 115200)
classifierModel = ModelTester(load_model("new_model.h5"))
main_print(serial_115200, classifierModel)
