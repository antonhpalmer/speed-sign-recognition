import csv

from keras.models import load_model

from classification.models import models
from classification.test.test import ModelTester
from classification.training.training import ModelTrainer


class Main:
    csv_path = 'results/cnn_model_test_results.csv'
    model = models.get_cnn_model()
    with open(csv_path, mode='w') as results_file:
        writer = csv.writer(results_file, delimiter=';')
        writer.writerow(['Epoch', 'Accuracy'])

    for epoch in range(1, 30):
        h5_filename = 'classification/models/cnn_model/cnn_model' + str(epoch) + '.h5'
        trainer = ModelTrainer('GTSRB/Final_Training/Images/', 0.01)
        trainer.train_model(model, h5_filename, 1)

        tester = ModelTester(model, 'GTSRB/Final_Test/Images/', 'GTSRB/GT-final_test.csv')
        accuracy = tester.test_using_dataset()

        with open(csv_path, mode='a') as results_file:
            writer = csv.writer(results_file, delimiter=';')
            writer.writerow([str(epoch), str(accuracy)])

        # model = load_model(h5_filename)

