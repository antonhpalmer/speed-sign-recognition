import csv
import os

from keras.models import load_model

from classification import preprocessing
from classification.models import models
from classification.test.test import ModelTester
from classification.training.training import ModelTrainer


class TestModelAccuracy:


    def create_test_for_model(self, model, model_name, epochs, learning_rate):
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
            trainer.train_model(imgs, labels, model, h5_filename, 1)

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

