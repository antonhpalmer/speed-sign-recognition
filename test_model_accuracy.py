import csv
import os
import matplotlib.pyplot as plt
from keras.models import load_model
from skimage import io
from classification import preprocessing
from classification.models import models
from classification.test.test import ModelTester
from classification.training.training import ModelTrainer


class TestModelAccuracy:

    model = models.get_model9()
    model_name = "model9_"
    epochs = 4
    learning_rate = 0.01

    tester = ModelTester(model)
    tester.create_test_files_for_model(model_name, epochs, learning_rate)


    # model_path = 'classification/models/' + model_name + '/'
    # csv_path = model_path + model_name + '.csv'
    #
    # # Testing the model for each of the saved h5 files (so for each epoch)
    # for epoch in range(13, 14):
    #     h5_filename = model_path + model_name + str(epoch) + '.h5'
    #     if not os.path.exists(h5_filename):
    #         continue
    #
    #     loaded_model = load_model(h5_filename)
    #     tester = ModelTester(loaded_model)
    #     accuracy = tester.test_using_dataset('GTSRB/Final_Test/Images/', 'GTSRB/GT-final_test.csv')
    #
    #     # Outputs test result to csv file
    #     with open(csv_path, mode='a', newline='') as results_file:
    #         writer = csv.writer(results_file, delimiter=';')
    #         writer.writerow([str(epoch), str(accuracy), str(learning_rate)])




