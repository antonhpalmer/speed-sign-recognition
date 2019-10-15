from classification.test.test import ModelTester
from detection.detect import detect
from validation.validator import validate
from keras.models import load_model
import serial

def send_signal(ser):
    ser.write(b'9')
    ser.write(b'\n')
    ser.readline()
    print("Signal written to serial")


classifier = ModelTester(load_model("classification/models/cnn_model/cnn_model8.h5"))
ser = serial.Serial('/dev/ttyACM1', 115200)
print("Ready to read from serial 115200")

while True:
    detected_img = detect(ser)
    print("Object was detected")
    validated = validate(detected_img)
    print("Object was validated: ", validated)
    if validated:
        new_speed = classifier.classify_single_image(detected_img.filename)
        print("detected sign is: ", new_speed)
        # update_speed(new_speed)
    send_signal(ser)
    break


