import csv
import os

from keras.models import load_model

from classification import preprocessing
from classification.models import models
from classification.test.test import ModelTester
from classification.training.training import ModelTrainer


class TestModelAccuracy:
    model = models.get_cnn_model()
    model_name = "cnn_model1"
    epochs = 10
    learning_rate = 0.005

    tester = ModelTester(model)
    tester.create_test_files_for_model(model_name, epochs, learning_rate)


