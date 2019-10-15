#  Copyright (c) 2019.
#  AAU, Student project group sw504e19, 2019.
#  Use this as reference to coding conventions in Python: https://github.com/kengz/python

import os

import numpy as np
import pandas as pd
from keras.preprocessing import image
from skimage import io

from classification import definitions, preprocessing


class ModelTester:

    def __init__(self, model):
        self.model = model

    def __get_label_name(self, class_indexes):
        str = ""
        for i in class_indexes:
            str += definitions.ID_SWITCHER.get(i, "Invalid class_id")
            str += ', '
        if len(str) > 0:
            return str[:-2]
        else:
            return str

    def __transform_test_image(self, image_path):
        img = image.load_img(image_path, target_size=(definitions.IMG_SIZE, definitions.IMG_SIZE))
        img = preprocessing.preprocess_img(img)
        img = np.expand_dims(img, axis=0)
        return img

    def classify_single_image(self, image_path):
        img = self.__transform_test_image(image_path)
        result = self.model.predict_classes(img)
        print(str(result[0]))
        return str(result[0])

    def classify_multiple_images(self, *args):
        imgs = []
        for image_path in args:
            imgs.append(self.__transform_test_image(image_path))
        result = self.model.predict_classes(imgs)
        print(self.__get_label_name(result))

    def test_using_dataset(self, dataset_path, csv_path):
        test = pd.read_csv(csv_path, sep=';')

        # Load test dataset
        x_test = []
        y_test = []

        for file_name, class_id in zip(list(test['Filename']), list(test['ClassId'])):
            img_path = os.path.join(dataset_path, file_name)
            x_test.append(preprocessing.preprocess_img(io.imread(img_path)))
            y_test.append(class_id)

        x_test = np.array(x_test)
        y_test = np.array(y_test)

        # predict and evaluate
        y_pred = self.model.predict_classes(x_test)
        acc = np.sum(y_pred == y_test) / np.size(y_pred)
        print("Test accuracy = {}".format(acc))
        return acc

    def print_model_summary(self):
        print(self.model.summary())
