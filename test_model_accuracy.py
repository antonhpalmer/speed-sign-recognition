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
    model = models.get_model1()
    model_name = "model1_"
    epochs = 10
    learning_rate = 0.01

    tester = ModelTester(model)
    tester.create_test_files_for_model(model_name, epochs, learning_rate)

