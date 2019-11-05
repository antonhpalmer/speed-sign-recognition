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
        return result[0]

    def classify_multiple_images(self, *args):
        imgs = []
        for image_path in args:
            imgs.append(self.__transform_test_image(image_path))
        result = self.model.predict_classes(imgs)
        return result

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

    def write_model_summary_to_file(self, file):
        return self.model.summary(print_fn=lambda x: file.write(x + '\n'))

    def __get_current_epoch(self, model_path, model_name):
        files = []
        for dirpath, dirnames, filenames in os.walk(model_path):
            files.extend(filenames)
            break

        epochs = []
        for filename in files:
            if ".h5" in filename and model_name in filename:
                epoch = filename[len(model_name):-3]
                epochs.append(int(epoch))

        if len(epochs) > 0:
            return max(epochs)
        else:
            return 0

    def __train_model_in_epoch_steps(self, model_path, model_name, learning_rate, current_epoch, epochs,
                                     training_dataset_path):
        # Training the model and saving a h5 file for each epoch
        imgs = []
        labels = []
        preprocessing.preprocess_all_images(training_dataset_path, imgs, labels)
        for epoch in range(current_epoch + 1, current_epoch + epochs + 1):
            h5_filename = model_path + model_name + str(epoch) + '.h5'
            trainer = ModelTrainer(training_dataset_path, learning_rate)
            trainer.train_model(imgs, labels, self.model, h5_filename, 1)

    def __test_and_output_results(self, csv_path, model_path, model_name, start_epoch, epochs, learning_rate,
                                  test_dataset_path, test_csv_path):
        # Create csv results file
        if not os.path.exists(csv_path):
            with open(csv_path, mode='w', newline='') as results_file:
                writer = csv.writer(results_file, delimiter=';')
                writer.writerow(['Epoch', 'Accuracy', 'Learning rate'])

        # Testing the model for each of the saved h5 files (so for each epoch)
        for epoch in range(start_epoch + 1, start_epoch + epochs + 1):
            h5_filepath = model_path + model_name + str(epoch) + '.h5'
            if not os.path.exists(h5_filepath):
                continue

            loaded_model = load_model(h5_filepath)
            tester = ModelTester(loaded_model)
            accuracy = tester.test_using_dataset(test_dataset_path, test_csv_path)

            # Outputs test result to csv file
            with open(csv_path, mode='a', newline='') as results_file:
                writer = csv.writer(results_file, delimiter=';')
                writer.writerow([str(epoch), str(accuracy), str(learning_rate)])

    def train_and_test_model(self, model_name, epochs, learning_rate, training_dataset_path, test_dataset_path,
                             test_csv_path):
        model_path = 'classification/models_new_dataset/' + model_name + '/'
        os.makedirs(model_path, exist_ok=True)
        csv_path = model_path + model_name + '.csv'
        current_epoch = self.__get_current_epoch(model_path, model_name)
        if current_epoch > 0:
            self.model = load_model(model_path + model_name + str(current_epoch) + '.h5')

        self.__train_model_in_epoch_steps(model_path, model_name, learning_rate, current_epoch, epochs,
                                          training_dataset_path)

        self.__test_and_output_results(csv_path, model_path, model_name, current_epoch, epochs, learning_rate,
                                       test_dataset_path, test_csv_path)


