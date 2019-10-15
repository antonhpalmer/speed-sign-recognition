from classification.test.test import ModelTester
from detection.detect import detect
from validation.validator import validate
from keras.models import load_model

classifier = ModelTester(load_model("classification/models/cnn_model/cnn_model8.h5"))

while True:
    detected_img = detect()
    if validate(detected_img):
        new_speed = classifier.classify_single_image(detected_img)
        # update_speed(new_speed)
