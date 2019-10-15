#  Copyright (c) 2019.
#  AAU, Student project group sw504e19, 2019.
#  Use this as reference to coding conventions in Python: https://github.com/kengz/python
import csv
import os

import numpy as np
import pandas as pd
from keras.preprocessing import image
from skimage import io
from keras.models import load_model

from classification import definitions, preprocessing
from classification.training.training import ModelTrainer


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

    def create_test_files_for_model(self, model_name, epochs, learning_rate):
        model_path = 'classification/models/' + model_name + '/'
        os.mkdir(model_path)
        csv_path = model_path + model_name + '.csv'

        # Training the model and saving a h5 file for each epoch
        imgs = []
        labels = []
        preprocessing.preprocess_all_images('GTSRB/Final_Training/Images/', imgs, labels)
        for epoch in range(1, epochs):
            h5_filename = model_path + model_name + str(epoch) + '.h5'
            trainer = ModelTrainer('GTSRB/Final_Training/Images/', learning_rate)
            trainer.train_model(imgs, labels, self.model, h5_filename, 1)

        # Create csv results file
        with open(csv_path, mode='w') as results_file:
            writer = csv.writer(results_file, delimiter=';')
            writer.writerow(['Epoch', 'Accuracy'])

        # Testing the model for each of the saved h5 files (so for each epoch)
        for epoch in range(1, epochs):
            h5_filename = model_path + model_name + str(epoch) + '.h5'
            loaded_model = load_model(h5_filename)
            tester = ModelTester(loaded_model)
            accuracy = tester.test_using_dataset('GTSRB/Final_Test/Images/', 'GTSRB/GT-final_test.csv')

            # Outputs test result to csv file
            with open(csv_path, mode='a') as results_file:
                writer = csv.writer(results_file, delimiter=';')
                writer.writerow([str(epoch), str(accuracy)])


