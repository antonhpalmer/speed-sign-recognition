import csv
import os
import matplotlib.pyplot as plt
import pandas as pd
from keras.models import load_model
from skimage import io
from classification import preprocessing, definitions
from classification.models import models
from classification.test.test import ModelTester
from classification.training.training import ModelTrainer
from keras.preprocessing import image
import numpy as np

class TestModelAccuracy:
    #
    # model = models.get_model10()
    # model_name = "model10_"
    # epochs = 4
    # learning_rate = 0.01
    #
    # tester = ModelTester(model)
    # tester.create_test_files_for_model(model_name, epochs, learning_rate)

    # for i in range(1, 9):
    #     tester = ModelTester(load_model('classification/models/cnn_model/cnn_model' + str(i) + '.h5'))
    #     tester.test_using_dataset('testdata/Images/', 'testdata/testdata_file.csv')

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

    # models_path = 'classification/models/'
    # for root, dirs, files in os.walk(models_path):
    #     basename = os.path.basename(root)
    #     if 'model' not in basename:
    #         continue
    #
    #     number_of_h5_files = 0
    #     for file in files:
    #         if '.h5' in file:
    #             number_of_h5_files += 1
    #
    #     print(basename + ':')
    #     model_name = basename
    #     model_path = models_path + model_name + '/'
    #     csv_path = model_path + model_name + '_pixy_dataset' + '.csv'
    #     tester = ModelTester(models.get_cnn_model())
    #     tester.test_and_output_results(csv_path, model_path, model_name, 0, number_of_h5_files, 0.01,
    #                                    'testdata/Images/', 'testdata/testdata_file.csv')


    epochs = 10
    learning_rate = 0.01
    training_dataset_path = 'test_data/training_images/'
    test_dataset_path = 'test_data/test_images/'
    test_csv_path = 'test_data/test_file.csv'

    model_switcher = {
        0: [models.get_cnn_model(), 'cnn_model_newdata'],
        1: []
    }

    for model_number in range(0, 11):
        if model_number == 0:
            model = models.get_cnn_model()
            model_name = 'cnn_model_newdata'
        else:
            model = models.get
        tester = ModelTester(model)
        tester.train_and_test_model(model_name, epochs, learning_rate, training_dataset_path, test_dataset_path,
                                test_csv_path)



