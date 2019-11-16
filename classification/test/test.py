#  Copyright (c) 2019.
#  AAU, Student project group sw504e19, 2019.
#  Use this as reference to coding conventions in Python: https://github.com/kengz/python

import numpy as np
from keras.preprocessing import image
from keras_preprocessing.image import ImageDataGenerator

from classification.definitions import IMG_SIZE


class ModelTester:

    def __init__(self, model):
        self.model = model

    def index_to_sign(self, index):
        index_to_sign_switcher = {
            0: 100,
            1: 110,
            2: 120,
            3: 30,
            4: 50,
            5: 60,
            6: 70,
            7: 80,
            8: 90
        }
        return index_to_sign_switcher.get(index)

    def classify_single_image(self, image_path):
        img = image.load_img(image_path, target_size=(IMG_SIZE, IMG_SIZE))
        img = np.expand_dims(img, axis=0)
        classes = self.model.predict(img)
        return self.index_to_sign(np.argmax(classes[0]))

    def evaluate_model(self, test_dir_path):
        test_datagen = ImageDataGenerator()
        test_iterator = test_datagen.flow_from_directory(test_dir_path, target_size=(IMG_SIZE, IMG_SIZE), shuffle=False)
        return self.model.evaluate(test_iterator)

    def write_model_summary_to_file(self, file):
        return self.model.summary(print_fn=lambda x: file.write(x + '\n'))



