import serial
from keras.models import load_model
from preprocessor.preproccesor import preprocess_image
from preprocessor.wrong_center_exception import WrongCenterException

from detection.pixy_serial_communication.serial_reader import update_speed
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

        validated_image = validate(detected_img)
        print("Object was validated: ", validated_image.is_valid)

        if validated_image.is_valid:
            try:
                preprocessed_img = preprocess_image(detected_img, validated_image.circle_center)
                new_speed = classifier.classify_single_image(preprocessed_img.filename, "grayscale")
                print("detected sign is: ", new_speed)
                update_speed(ser, new_speed)
            except WrongCenterException:
                print("Center coordinate is surrounded by red pixels")


def main(ser, classifier):
    while True:
        wakeup_arduino(ser)

        detected_img = detect(ser)

        validated, coordinates = validate(detected_img)

        if validated:
            try:
                preprocessed_img = preprocess_image(detected_img, coordinates)
                new_speed = classifier.classify_single_image(preprocessed_img.filename, "grayscale")
                update_speed(ser, new_speed)
            except WrongCenterException:
                break


serial_115200 = serial.Serial('/dev/ttyACM0', 115200)
classifierModel = ModelTester(load_model("classification/systematic_test_binary/model_doubleconv_64_act=relu_opt=adam_ker=3_pad=same_drop=20/model_doubleconv_64_act=relu_opt=adam_ker=3_pad=same_drop=20.h5"))
main_print(serial_115200, classifierModel)
