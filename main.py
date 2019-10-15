from classification.test.test import ModelTester
from detection.detect import detect
from validation.validator import validate
from keras.models import load_model
import serial


classifier = ModelTester(load_model("classification/models/cnn_model/cnn_model8.h5"))
ser = serial.Serial('/dev/ttyACM0', 115200)

while True:
    detected_img = detect()
    print("Object was detected")
    ser.write(b'd')
    validated = validate(detected_img)
    print("Object was validated: ", validated)
    if validated:
        new_speed = classifier.classify_single_image(detected_img.filename)
        print("detected sign is: ", new_speed)
        # update_speed(new_speed)

