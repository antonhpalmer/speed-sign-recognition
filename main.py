import serial
from PIL import Image
from keras.models import load_model
from preprocessor.preproccesor import preprocess_image
from preprocessor.wrong_center_exception import WrongCenterException

from detection.pixy_serial_communication.serial_communication import update_speed, wakeup_arduino
from classification.test.test import ModelTester
from detection.detect import detect
from validation.validator import validate

from video_demo.display_signs import display_signs


def main_print(ser, classifier):
    print("Ready to read from serial 115200")
    while True:
        wakeup_arduino(ser)
        print("Waking up arduino...")
        detected_img = detect(ser)
        print("Object was detected")

        validated_img = validate(detected_img)
        print("Object was validated: ", validated_img.is_valid)

        if validated_img.is_valid:
            try:
                preprocessed_img = preprocess_image(detected_img, validated_img.circle_center)
                new_speed = classifier.classify_single_image(preprocessed_img.filename, "grayscale")
                display_signs(validated_img, preprocessed_img, new_speed)
                print("detected sign is: ", new_speed)
                update_speed(ser, new_speed)
            except WrongCenterException:
                print("Center coordinate is surrounded by red pixels")
        else:
            display_signs(validated_img, Image.open("video_demo/speedsign0.png"), 0)


def main(ser, classifier):
    while True:
        wakeup_arduino(ser)

        detected_img = detect(ser)

        validated_img = validate(detected_img)

        if validated_img.is_valid:
            try:
                preprocessed_img = preprocess_image(detected_img, validated_img.circle_center)
                new_speed = classifier.classify_single_image(preprocessed_img.filename, "grayscale")
                update_speed(ser, new_speed)
            except WrongCenterException:
                break


serial_115200 = serial.Serial('/dev/ttyACM0', 115200)
classifierModel = ModelTester(load_model("classification/systematic_test_binary/model_doubleconv_64_opt=adam_ker=3_drop=20/model_doubleconv_64_act=relu_opt=adam_ker=3_pad=same_drop=20.h5"))
main_print(serial_115200, classifierModel)
