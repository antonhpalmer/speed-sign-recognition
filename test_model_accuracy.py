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

    model = models.get_model7()
    model_name = "model7_"
    epochs = 8
    learning_rate = 0.01

    tester = ModelTester(model)
    tester.create_test_files_for_model(model_name, epochs, learning_rate)




